def newcorner(rec_axes, rec_size, width, umap, rmap, type):
    temp_axes = [0,None]
    point = 0
    ctemp = []
    new = []
    if type == 'up':
        u = 1
        r = 0
        map1 = umap
        map2 = rmap
        axes_init = [width - rec_axes[0] - rec_size[0],None]
    elif type == 'right':
        u = 0
        r = 1
        map1 = rmap
        map2 = umap
        axes_init = [width,None]
    else:
        return 0,0
    temp_axes[:] = axes_init[:]

    for i in range(len(map1)):
        if(rec_axes[u] + rec_size[u] > map1[i][u]):
            if(point == 0):
                point = i+1
            if(map1[i][r]-map1[i][r+2] <= rec_axes[r] + rec_size[r] < map1[i][r]):
                for j in range(len(map2)):
                    if(rec_axes[r] + rec_size[r] < map2[j][r]):
                        if(map1[i][u] < map2[j][u] < rec_axes[u] + rec_size[u]):
                            for k in range(j+1,len(map2)):
                                if(rec_axes[r] + rec_size[r] < map2[k][r] and map2[k][u] > map2[j][u]):
                                    break
                                if(rec_axes[r] + rec_size[r] >= map2[k][r] or k == len(map2)-1):
                                    ctemp.append(map2[j][u])
                                    break
                    else:
                        break
                ctemp.append(map1[i][u])
                ctemp = ctemp[::-1]
                for j in range(len(map1)):
                    if(map1[i][u] < map1[j][u]):
                        if(map1[j][r] - map1[j][r+2] <= rec_axes[r] + rec_size[r] < map1[j][r]):
                            if((u == 1 and temp_axes[u] is None) or temp_axes[u] > map1[j][u] - map1[j][u+2]):
                                temp_axes[u] = map1[j][u] - map1[j][u+2]
                    else:
                        break
                for j in range(len(ctemp)):
                    temp_axes[r] = axes_init[r]
                    for k in range(len(map2)):
                        if(rec_axes[r] + rec_size[r] < map2[k][r]):
                            if(map2[k][u] - map2[k][u+2] <= ctemp[j] < map2[k][u]):
                                if((r == 1 and temp_axes[r] is None) or temp_axes[r] > map2[k][r] - map2[k][r+2] - rec_axes[r] - rec_size[r]):
                                    temp_axes[r] = map2[k][r] - map2[k][r+2] - rec_axes[r] - rec_size[r]
                        else:
                            break
                    if(r == 0 and temp_axes[r] != 0):
                        new.append([rec_axes[r] + rec_size[r],ctemp[j],temp_axes[r],temp_axes[u]])
                        if(temp_axes[u] is not None):
                            new[len(new)-1][3] -= ctemp[j]
                    if(u == 0 and temp_axes[u] - ctemp[j] != 0):
                        new.append([ctemp[j],rec_axes[r] + rec_size[r],temp_axes[u]-ctemp[j],temp_axes[r]])
                break
    else:
        if(u == 1):
            temp = [rec_axes[1],rec_size[1]]
            rec_axes[1] = 0
            rec_size[1] = 0
        if(r == 1):
            temp = [rec_axes[0],rec_size[0]]
            rec_axes[0] = 0
            rec_size[0] = 0
        temp_axes[0] = width - rec_axes[0] - rec_size[0]
        for i in range(len(rmap)):
            if(rec_axes[0] + rec_size[0] < rmap[i][0]):
                if(rmap[i][1] - rmap[i][3] <= rec_axes[1] + rec_size[1] < rmap[i][1]):
                    if(temp_axes[0] > rmap[i][0] - rmap[i][2] - rec_axes[0] - rec_size[0]):
                        temp_axes[0] = rmap[i][0] - rmap[i][2] - rec_axes[0] - rec_size[0]
            else:
                break
        temp_axes[1] = None
        for i in range(len(umap)):
            if(rec_axes[1] + rec_size[1] < umap[i][1]):
                if(umap[i][0]-umap[i][2] <= rec_axes[0] + rec_size[0] < umap[i][0]):
                    if(temp_axes[1] is None or temp_axes[1] > umap[i][1] - umap[i][3] - rec_axes[1] - rec_size[1]):
                        temp_axes[1] = umap[i][1] - umap[i][3] - rec_axes[1] - rec_size[1]
            else:
                break
        if(temp_axes[0] != 0):
            new.append([rec_axes[0] + rec_size[0],rec_axes[1] + rec_size[1],temp_axes[0],temp_axes[1]])
        if(u == 1):
            rec_axes[1] = temp[0]
            rec_size[1] = temp[1]
        if(r == 1):
            rec_axes[0] = temp[0]
            rec_size[0] = temp[1]
    return point, new

