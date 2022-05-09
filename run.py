from matplotlib.colors import rgb2hex
from people import *
from kapao import *
from communication import *
import random
import cv2



if __name__ == '__main__':
    # com = Communication(myip='192.168.0.110', receiveport=8000, sendip ='192.168.0.100', sendport=8100)
    com = Communication(myip='localhost', receiveport=8000, sendip ='localhost', sendport=8100)
    com.start()

    kapao = Kapao()
    kapao.init()

    
    classes = ['CHINCHIN', 'DIABLE', 'COMBATTANT', 'ST. GEORGE', '']
    # classes = ['ACTION 1', 'ACTION 2', 'ACTION 3', 'ACTION 4', '']

    colors = [(204, 204, 0), (255, 51, 255)]

    capture = [0, 1, './data/test.mp4'][2]
     
    if type(capture) is int:
        cap = cv2.VideoCapture(capture, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(capture)

    cap.set(3, 1920)
    cap.set(4, 1080)

    xtargets = [500, 1320]
    ytarget = 900

    ret, frame = cap.read()
    people = People()
    pause = False
    f = 0
    while ret:
        boxes, poses = kapao.predict(frame)
        people_tmp = People()
        for j, (box, pose) in enumerate(zip(boxes, poses)):
            position = (np.array(pose[11]) + np.array(pose[12]))/2.
            position = position[:-1]

            com_pose = -1
            if abs(position[0] - xtargets[0]) <= 100 and abs(box[3] - ytarget) <= 100:
                com_pose = 0
            elif abs(position[0] - xtargets[1]) <= 100 and abs(box[3] - ytarget) <= 100:
                com_pose = 1

            if com_pose in com.list_of_people_to_analyze:
                active = True
            else:
                active = False

            people_tmp.add_person(pose, box, active=active)

        if not pause:
            people.track(people_tmp.people, smallest=100)

            for person in people.people:
                if person.active:
                    person.compute_features()
                    x1, y1, x2, y2 = person.box

                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), thickness=1)
                    cv2.putText(frame, 'ID_' + str(person.id), (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    # if len(person.feature) > 5:
                    #     cv2.putText(frame, classes[person.most_frequent(person.feature[-5:])[0]], (int(x2), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, colors[person.id], 1, cv2.LINE_AA)
                    
                    if abs(person.position[0] - xtargets[0]) <= 100:
                        cv2.circle(frame, (xtargets[0], ytarget), 100, colors[0], -1)
                        # Position of the text to be displayed inside the circle
                        textsize = cv2.getTextSize(classes[person.get_feature()], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                        c_disp_x = xtargets[0]-int(textsize[0]/2)
                        c_disp_y = ytarget-int(textsize[1]/2)
                        cv2.putText(frame, classes[person.get_feature()], (c_disp_x, c_disp_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

                    elif abs(person.position[0] - xtargets[1]) <= 100:
                        cv2.circle(frame, (xtargets[1], ytarget), 100, colors[1], -1)
                        # Position of the text to be displayed inside the circle
                        textsize = cv2.getTextSize(classes[person.get_feature()], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                        c_disp_x = xtargets[1]-int(textsize[0]/2)
                        c_disp_y = ytarget-int(textsize[1]/2)
                        cv2.putText(frame, classes[person.get_feature()], (c_disp_x, c_disp_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    # if person.get_feature() != 4:

                    if abs(person.position[0] - xtargets[0]) <= 100:
                        com_pose = 0
                    elif abs(person.position[0] - xtargets[1]) <= 100:
                        com_pose = 1

                    if com_pose in com.list_of_people_to_communicate:
                        person.feature = [x for x in person.feature if x != 4]
                        message = str(com_pose) + ' ' + str(person.get_feature())
                        message = [com_pose, person.get_feature()]
                        com.send(message)
                        people.people[people.index_by_id(person.id)].reset_feature()
                        com.list_of_people_to_analyze.remove(com_pose)
                        com.list_of_people_to_communicate.remove(com_pose)
                    
                    # Draw Skeleton
                    for seg in kapao.data['segments'].values():
                        pt1 = (int(person.pose[seg[0], 0]), int(person.pose[seg[0], 1]))
                        pt2 = (int(person.pose[seg[1], 0]), int(person.pose[seg[1], 1]))
                        cv2.line(frame, pt1, pt2, (255, 255, 255), 3)

            cv2.circle(frame, (xtargets[0], ytarget), 100, (255, 255, 255), 2)
            cv2.circle(frame, (xtargets[1], ytarget), 100, (255, 255, 255), 2)

        # frame = cv2.flip(frame, 1)
        cv2.imshow('ADD', frame)
        k = cv2.waitKey(10)
        if k == ord('q'):
            break
        if k == ord('s'):
            com.start_reco = not com.start_reco
            com.list_of_people_to_analyze = [0, 1]
        if k == ord('p'):
            com.stop_reco = True
            com.list_of_people_to_communicate = [0]

        if k == ord(' '):
            pause = not pause
        if k == ord('c'):
            colors = []
            for i in range(1000):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                colors.append([r, g, b])
        if k == ord('1'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 300)
            res, frame = cap.read()
        if k == ord('2'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 450)
            res, frame = cap.read()
        if k == ord('3'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 600)
            res, frame = cap.read()
        if k == ord('4'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 750)
            res, frame = cap.read()
        if k == ord('k'):
            classes = ['ACTION 1', 'ACTION 2', 'ACTION 3', 'ACTION 4', '']
        if k == ord('l'):
            classes = ['CHINCHIN', 'DIABLE', 'COMBATTANT', 'ST. GEORGE', '']

        if not pause:
            ret, frame = cap.read()
            f += 1

    cv2.destroyAllWindows()
    cap.release()
