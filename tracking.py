d = 0 
tracking_points = []
id = 1
time_life = 15
def dang_ki(point):
    global id
    tracking_points.append({
                "point": point,
                "distance": d,
                "check_calc_speed": False,
                "id": id,
                "life_cycle": time_life,
                "speed":0
                })
    id += 1

   
def cap_nhap(centers):
    if tracking_points == []:
        for center in centers:
            # print(f">>> center_point_tracking: {(center[0], center[1])}")
            dang_ki(center)       
    else:
        for point in tracking_points:
            point['life_cycle'] -= 1

        for pt in tracking_points:
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
    
      