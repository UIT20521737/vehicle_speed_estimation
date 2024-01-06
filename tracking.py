d = 0 
tracking_points = []
id = 1
time_life = 15
# Frame 65: 
# (569, 365)
# Frame 66: 
# (1662, 890)
# (563, 336)

# Frame 292:
# (393, 243)
# (1286, 194)
# (1691, 153)
# Frame 293:
# (1273, 168)
# (411, 202)
# DANG KI
def dang_ki(point):
    global id
    tracking_points.append({
                "point": point,
                "distance": d,
                "isExist": True,
                "id": id,
                "life_cycle": time_life
                })
    id += 1
    # print(">>> id tracking: ", id)
   
def cap_nhap(centers):
    if tracking_points == []:
        for center in centers:
            print(f">>> center_point_tracking: {(center[0], center[1])}")
            dang_ki(center)       
    else:
        for point in tracking_points:
            point['life_cycle'] -= 1
            if 430//3 <= point['point'][1] <= 450//3:
                xoa(point['point'])
        # print(f">>> con laij gi", tracking_points)
        tracking_points_copy = tracking_points.copy()
        # print(f">>> con laij gi copy", tracking_points_copy)
        
        for pt in tracking_points_copy:
            (x,y) = pt['point']
            distances = []
            if centers == []:
                break
            
            for center in centers:
                (x1,y1) = center
                d = ((x1 - x)**2 + (y1 - y)**2)**0.5
                
                distances.append(d)
            min_distance = min(distances)
            index_min_distance = distances.index(min_distance)
            index = tracking_points.index(pt)
            if min_distance < 350//3:
                tracking_points[index]["life_cycle"] +=1
                tracking_points[index]["distance"] = distances[index_min_distance]
                tracking_points[index]["point"] = centers[index_min_distance]
                # print(">>>>>>>",tracking_points[index]["distance"])
                # print(">>>",distances[index_min_distance])
                del centers[index_min_distance]
        for pt in tracking_points:  
            index = tracking_points.index(pt)
            if tracking_points[index]["life_cycle"] <= 0:
                xoa(tracking_points[index]["point"])
                
                
        # print(">>> con lai tracking_points ",tracking_points)
        if len(centers) != 0:
            for center in centers:
                # print(f">>> center_point_tracking: {(center[0], center[1])}")    
                dang_ki(center)   
               
def xoa(point):
    for x in tracking_points:
        if point == x['point']:
            index = tracking_points.index(x)
            del tracking_points[index]
if __name__ == "__main__":
    
    centers = [(460, 646)]
    cap_nhap(centers)
    print(f"tracking_points {tracking_points}")
    print(id)
    
    centers = [(0, 0)]
    cap_nhap(centers)
    print(f"tracking_points {tracking_points}")
    print(id)
    # centers = [(400, 400 ),(411, 202)]
    # cap_nhap(centers)
    # print(f"tracking_points {tracking_points}")
    
      