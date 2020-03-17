import sys, random
import svgwrite
import find
from svgwrite import cm,mm

args = sys.argv

num_blocks = int(args[1])
rec = []

mu = 5
sigma = 2
for i in range(num_blocks):
    bl_size_x = int(random.normalvariate(mu, sigma))
    if bl_size_x < 0:
        bl_size_x = -bl_size_x
    if bl_size_x == 0:
        bl_size_x = 1
    bl_size_y = int(random.normalvariate(mu, sigma))
    if bl_size_y < 0:
        bl_size_y = -bl_size_y
    if bl_size_y == 0:
        bl_size_y = 1
    rec.append([bl_size_x,bl_size_y])
    
    
width = int(args[2])
# [x_axis,y_axis,x_enable,y_enable]
corner = [[0,0,width,None]]
newcorner = []
ctemp = []
delete = []
# [x,y,length,width]
# _______  ________.(x,y)
#  width  |\\\\\\\\|
# -------  --------
#         | length |
umap = [] # rec's map sorted on y
rmap = [] # rec's map sorted on x
for i in range(len(rec)):
    for j in range(len(corner)):
        if(rec[i][0] <= corner[j][2] and (corner[j][3] is None or rec[i][1] <= corner[j][3])):
            cur_rec = rec[i]
            cur_axes = corner[j][0:2]
            upoint, newcorner = find.newcorner(cur_axes, cur_rec, width, umap, rmap, 'up')
            rpoint, ctemp = find.newcorner(cur_axes, cur_rec, width, umap, rmap, 'right')
            newcorner = newcorner + ctemp

            ctemp = [cur_axes[0]+cur_rec[0],cur_axes[1]+cur_rec[1],cur_rec[0],cur_rec[1]]
            if(upoint == 0):
                umap.append(ctemp)
            else:
                umap.insert(upoint-1,ctemp)
            if(rpoint == 0):
                rmap.append(ctemp)
            else:
                rmap.insert(rpoint-1,ctemp)

            delete = []
            for l in range(len(corner)):
                if(cur_axes[0] <= corner[l][0] < cur_axes[0]+cur_rec[0]):
                    if(cur_axes[1] <= corner[l][1] < cur_axes[1]+cur_rec[1]):
                        delete.append(l)
                        continue
                if(corner[l][0] < cur_axes[0]+cur_rec[0] and corner[l][0]+corner[l][2] > cur_axes[0]):
                    if(corner[l][1] < cur_axes[1]+cur_rec[1] and (corner[l][3] is None or corner[l][1]+corner[l][3] > cur_axes[1])):
                        if(corner[l][1] >= cur_axes[1]):
                            corner[l][2] = cur_axes[0]-corner[l][0]
                        elif(corner[l][0] >= cur_axes[0]):
                            corner[l][3] = cur_axes[1]-corner[l][1]
                        else:
                            for k in range(l+1,len(corner)):
                                if(corner[l][1] == corner[k][1]):
                                    if(corner[l][0] < corner[k][0] < corner[l][0]+corner[l][2]):
                                        delete.append(k)
                                if(corner[l][0] == corner[k][0]):
                                    if(corner[l][1] < corner[k][1] < corner[l][1]+corner[l][3]):
                                        delete.append(k)
                                        break
                            newcorner.append([corner[l][0],corner[l][1],cur_axes[0]-corner[l][0],corner[l][3]])
                            corner[l][3] = cur_axes[1]-corner[l][1]
                                    

            for l,num in enumerate(delete):
                del(corner[num - l])
            temp = 0
            for l in range(len(newcorner)):
                if(newcorner[l][0] == width):
                    continue
                for k in range(temp,len(corner)):
                    if(corner[k] == newcorner[l]):
                        break
                    if((corner[k][1] == newcorner[l][1] and corner[k][0] > newcorner[l][0]) or corner[k][1] > newcorner[l][1]):
                        corner.insert(k,newcorner[l])
                        temp = k+1
                        break
                else:
                    corner.append(newcorner[l])
                    temp = len(corner)
            break

leftup = umap[0][1] + 2
dwg = svgwrite.Drawing(filename="result.svg")
for i in range(len(umap)):
    dwg.add(dwg.rect(insert=((umap[i][0]-umap[i][2])*(100/leftup)*mm,(leftup-umap[i][1])*(100/leftup)*mm),size=(umap[i][2]*(100/leftup)*mm,umap[i][3]*(100/leftup)*mm),fill='black',fill_opacity=0.4,stroke='black'))
for i in range(len(corner)):
    if(corner[i][3] is None):
        corner[i][3] = umap[0][1] + 2 - corner[i][1]
    dwg.add(dwg.rect(insert=(corner[i][0]*(100/leftup)*mm,(leftup-corner[i][1]-corner[i][3])*(100/leftup)*mm),size=(corner[i][2]*(100/leftup)*mm,corner[i][3]*(100/leftup)*mm),fill='red',fill_opacity=0.2,stroke='red'))
dwg.save()
