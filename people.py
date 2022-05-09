import math
import numpy as np
# from sklearn.neighbors import NearestCentroid

class Person():
    def __init__(self, pose=None, pose_t0=None, box=None, position=None, feature=[], id=-1, active=False):
        self.pose = pose
        self.pose_t0 = pose_t0
        self.box = box
        self.position = position
        self.id = id
        self.active = active
        self.feature = feature
        self.feature_buffer = 12
        self.nodes = {'Nose': 0,
                      'LEye': 1,
                      'REye': 2,
                      'LNose': 3,
                      'RNose': 4,
                      'LShoulder': 5,
                      'RShoulder': 6,
                      'LElbow': 7,
                      'RElbow': 8,
                      'LWrist': 9,
                      'RWrist': 10,
                      'LHip': 11,
                      'RHip': 12,
                      'LKnee': 13,
                      'RKnee': 14,
                      'LFoot': 15,
                      'RFoot': 16}

    def init(self, pose, box):
        self.pose = pose
        self.pose_t0 = pose
        self.box = box
        self.feature = []
        # position = (np.array([box[0], box[1]])[:-1] + np.array([box[2], box[3]])[:-1])/2.
        position = (np.array(pose[self.nodes['LHip']]) + np.array(pose[self.nodes['RHip']]))/2.
        position = position[:-1]
        self.position = position

    def update(self, person):
        self.pose_t0 = self.pose
        self.pose = person.pose
        self.box = person.box
        self.position = person.position
        self.active = person.active

    def update_status(self, active):
        self.active = active

    def set_pose(self, pose):
        self.pose_t0 = self.pose
        self.pose = pose

    def set_box(self, box):
        self.box = box

    def set_id(self, id):
        self.id = id

    def get_position(self):
        return self.position

    def get_pose(self):
        return self.pose

    def get_box(self):
        return self.box

    def angle(self, p1, p2):
        if not p1.any() or not p2.any():
            return None
        uv1 = p1 / np.linalg.norm(p1)
        uv2 = p2 / np.linalg.norm(p2)
        dot_product = np.dot(uv1, uv2)
        ang = np.arccos(dot_product) # rad
        return ang

    def distance(self, p1, p2):
        return np.linalg.norm(p1-p2)

    def velocity(self, p0, p1):
        return math.sqrt(sum((p1-p0)**2))

    def most_frequent(self, List):
        mf = max(set(List), key = List.count)
        return mf, List.count(mf)

    def get_feature(self):
        if len(self.feature) > 0:
            mf, _ = self.most_frequent(self.feature)
        else:
            mf = 4
        return mf

    def reset_feature(self):
        self.feature = []



    def chinchin(self):
        # FEATURES PART
        ang1 = self.angle(self.pose[self.nodes['LShoulder']] - self.pose[self.nodes['LHip']], 
                          self.pose[self.nodes['LKnee']] - self.pose[self.nodes['LHip']])
        ang2 = self.angle(self.pose[self.nodes['RShoulder']] - self.pose[self.nodes['RHip']], 
                          self.pose[self.nodes['RKnee']] - self.pose[self.nodes['RHip']])
        # ang3 = self.angle(self.pose[self.nodes['LHip']] - self.pose[self.nodes['LShoulder']], 
        #                   self.pose[self.nodes['LElbow']] - self.pose[self.nodes['LShoulder']])
        # ang4 = self.angle(self.pose[self.nodes['RHip']] - self.pose[self.nodes['RShoulder']], 
        #                   self.pose[self.nodes['RElbow']] - self.pose[self.nodes['RShoulder']])
        ang5 = self.angle(self.pose[self.nodes['LWrist']] - self.pose[self.nodes['RWrist']], 
                          self.pose[self.nodes['LShoulder']] - self.pose[self.nodes['RShoulder']])
        ang6 = self.angle(self.pose[self.nodes['LWrist']] - self.pose[self.nodes['LElbow']], 
                          self.pose[self.nodes['LShoulder']] - self.pose[self.nodes['LElbow']])
        ang7 = self.angle(self.pose[self.nodes['RWrist']] - self.pose[self.nodes['RElbow']], 
                          self.pose[self.nodes['RShoulder']] - self.pose[self.nodes['RElbow']])

        # dist1 = self.distance(self.pose[self.nodes['LWrist']], self.pose[self.nodes['RWrist']])
        # dist2 = self.distance(self.pose[self.nodes['LElbow']], self.pose[self.nodes['RElbow']])
        # print('chinchin', ang4)
        # (ang1 is not None and ang2 is not None and ang3 is not None and ang4 is not None and dist1 is not None and dist2 is not None) and 
        # print(self.id, dist1 <= dist2)
        # if (ang1 < 2.6 or ang2 < 2.6) and \
        #     (ang3 < 1 and ang4 < 1) and \
        #     dist1 <= dist2 and \
        #     self.pose[self.nodes['LWrist']][1] < self.pose[self.nodes['LHip']][1] and \
        #     self.pose[self.nodes['RWrist']][1] < self.pose[self.nodes['RHip']][1]:
        #     self.feature.append(0)
        #     return True
        # else:
        #     return False
        dist3 = self.distance(self.pose[self.nodes['LFoot']], self.pose[self.nodes['LHip']])
        dist4 = self.distance(self.pose[self.nodes['RFoot']], self.pose[self.nodes['RHip']])

        if (ang1 < 2.6 or ang2 < 2.6) and (ang5 < 0.6) and (ang6 < 2.5 or ang7 < 2.5):# and dist3 > 100 and dist4 > 100:
            self.feature.append(0)
            return True
        else:
            return False


    def chinchin2(self):
        dist0 = self.distance(self.pose[self.nodes['LHip']], self.pose[self.nodes['LKnee']])
        dist1 = self.distance(self.pose[self.nodes['LShoulder']], self.pose[self.nodes['LWrist']])/dist0
        dist2 = self.distance(self.pose[self.nodes['RShoulder']], self.pose[self.nodes['RWrist']])/dist0
        dist3 = self.distance(self.pose[self.nodes['LWrist']], self.pose[self.nodes['RWrist']])/dist0

        ang1 = self.angle(self.pose[self.nodes['LHip']] - self.pose[self.nodes['LKnee']], 
                          self.pose[self.nodes['LFoot']] - self.pose[self.nodes['LKnee']])
        ang2 = self.angle(self.pose[self.nodes['RHip']] - self.pose[self.nodes['RKnee']], 
                          self.pose[self.nodes['RFoot']] - self.pose[self.nodes['RKnee']])

        if dist1 < 0.8 and dist2 < 0.8 and dist3 < 0.9 and (ang1 < 2.8 or ang2 < 2.8):
            self.feature.append(0)
            return True
        else:
            return False


    def habitant(self):
        ang1 = self.angle(self.pose[self.nodes['LElbow']] - self.pose[self.nodes['LShoulder']], 
                          self.pose[self.nodes['LHip']] - self.pose[self.nodes['LShoulder']])
        ang2 = self.angle(self.pose[self.nodes['RElbow']] - self.pose[self.nodes['RShoulder']], 
                          self.pose[self.nodes['RHip']] - self.pose[self.nodes['RShoulder']])

        if ang1 > 2.3 and ang2 > 2.3:
            self.feature.append(2)
            return True
        else:
            return False

    def diable(self):
        ang1 = self.angle(self.pose[self.nodes['LHip']] - self.pose[self.nodes['LKnee']], 
                          self.pose[self.nodes['LFoot']] - self.pose[self.nodes['LKnee']])
        ang2 = self.angle(self.pose[self.nodes['RHip']] - self.pose[self.nodes['RKnee']], 
                          self.pose[self.nodes['RFoot']] - self.pose[self.nodes['RKnee']])

        

        ang1_t0 = self.angle(self.pose_t0[self.nodes['LShoulder']] - self.pose_t0[self.nodes['LElbow']], 
                          self.pose_t0[self.nodes['LWrist']] - self.pose_t0[self.nodes['LElbow']])
        ang1_t1 = self.angle(self.pose[self.nodes['LShoulder']] - self.pose[self.nodes['LElbow']], 
                          self.pose[self.nodes['LWrist']] - self.pose[self.nodes['LShoulder']])

        ang2_t0 = self.angle(self.pose_t0[self.nodes['RShoulder']] - self.pose_t0[self.nodes['RElbow']], 
                          self.pose_t0[self.nodes['RWrist']] - self.pose_t0[self.nodes['RElbow']])
        ang2_t1 = self.angle(self.pose[self.nodes['RShoulder']] - self.pose[self.nodes['RElbow']], 
                          self.pose[self.nodes['RWrist']] - self.pose[self.nodes['RShoulder']])

        ang3_t0 = self.angle(self.pose_t0[self.nodes['LElbow']] - self.pose_t0[self.nodes['LShoulder']], 
                          self.pose_t0[self.nodes['LHip']] - self.pose_t0[self.nodes['LShoulder']])
        ang3_t1 = self.angle(self.pose[self.nodes['LElbow']] - self.pose[self.nodes['LShoulder']], 
                          self.pose[self.nodes['LHip']] - self.pose[self.nodes['LShoulder']])
        ang4_t0 = self.angle(self.pose_t0[self.nodes['RElbow']] - self.pose_t0[self.nodes['RShoulder']], 
                          self.pose_t0[self.nodes['RHip']] - self.pose_t0[self.nodes['RShoulder']])
        ang4_t1 = self.angle(self.pose[self.nodes['RElbow']] - self.pose[self.nodes['RShoulder']], 
                          self.pose[self.nodes['RHip']] - self.pose[self.nodes['RShoulder']])

        

        vang1 = abs(ang1_t1 - ang1_t0)
        vang2 = abs(ang2_t1 - ang2_t0)
        vang3 = abs(ang3_t1 - ang3_t0)
        vang4 = abs(ang4_t1 - ang4_t0)

        wrist_under_shoulder = (self.pose[self.nodes['RWrist']][1] > self.pose[self.nodes['RShoulder']][1]) and (self.pose[self.nodes['LWrist']][1] > self.pose[self.nodes['LShoulder']][1])
        # print('[D]', self.id, wrist_under_shoulder)
        # if ((vang1 > 0.05 and vang2 < 0.015) or (vang2 > 0.05 and vang1 < 0.015)) and wrist_under_shoulder :#and ang1 > 3 and ang2 > 3:
        if ((vang1 > 0.3 and vang2 < 0.2) or (vang2 > 0.3 and vang1 < 0.2)) and wrist_under_shoulder and ang1 > 3 and ang2 > 3:
            self.feature.append(1)
            return True
        else:
            return False


    def diable2(self):

        vx_lelbow = abs(self.pose[self.nodes['LElbow']][0] - self.pose_t0[self.nodes['LElbow']][0])
        vx_relbow = abs(self.pose[self.nodes['RElbow']][0] - self.pose_t0[self.nodes['RElbow']][0])

        ang_l_e_sh_h = self.angle(self.pose[self.nodes['LWrist']] - self.pose[self.nodes['LShoulder']], 
                          self.pose[self.nodes['LHip']] - self.pose[self.nodes['LShoulder']])

        ang_r_e_sh_h = self.angle(self.pose[self.nodes['RWrist']] - self.pose[self.nodes['RShoulder']], 
                          self.pose[self.nodes['RHip']] - self.pose[self.nodes['RShoulder']])

        ang_l_w_e_sh = self.angle(self.pose[self.nodes['LWrist']] - self.pose[self.nodes['LElbow']], 
                          self.pose[self.nodes['LShoulder']] - self.pose[self.nodes['LElbow']])

        ang_r_w_e_sh = self.angle(self.pose[self.nodes['RWrist']] - self.pose[self.nodes['RElbow']], 
                          self.pose[self.nodes['RShoulder']] - self.pose[self.nodes['RElbow']])


        dist_lk_rk_t1 = self.distance(self.pose[self.nodes['LKnee']], self.pose[self.nodes['RKnee']])
        dist_lk_rk_t0 = self.distance(self.pose_t0[self.nodes['LKnee']], self.pose_t0[self.nodes['RKnee']])

        vdk = abs(dist_lk_rk_t1 - dist_lk_rk_t0)
        # print(self.id, vdk)

        # print('DIABLE2', self.id, vx_lelbow, vx_relbow, ang_l_e_sh_h, ang_r_e_sh_h, vdk)
        # print(10, math.pi/5)
        # print(ang_l_w_e_sh)

        if ((vx_lelbow > 5 and ang_r_e_sh_h < math.pi/6 and ang_r_w_e_sh > math.pi*0.7) or (vx_relbow > 5 and ang_l_e_sh_h < math.pi/6 and ang_l_w_e_sh > math.pi*0.7)) and vdk < 1:
            self.feature.append(1)
            print(self.id, "DIABLE")
            return True
        else:
            print(' ')
            return False

        
    def sgeorge(self):

        ang1 = self.angle(self.pose[self.nodes['LElbow']] - self.pose[self.nodes['LWrist']], 
                          self.pose[self.nodes['RElbow']] - self.pose[self.nodes['RWrist']])
        ang2 = self.angle(self.pose[self.nodes['LHip']] - self.pose[self.nodes['LKnee']], 
                          self.pose[self.nodes['LFoot']] - self.pose[self.nodes['LKnee']])
        ang3 = self.angle(self.pose[self.nodes['RHip']] - self.pose[self.nodes['RKnee']], 
                          self.pose[self.nodes['RFoot']] - self.pose[self.nodes['RKnee']])

        dist1 = self.distance(self.pose[self.nodes['LShoulder']], self.pose[self.nodes['LKnee']])
        dist2 = self.distance(self.pose[self.nodes['LShoulder']], self.pose[self.nodes['LHip']])
        dist3 = self.distance(self.pose[self.nodes['LHip']], self.pose[self.nodes['LKnee']])

        dist4 = self.distance(self.pose[self.nodes['RShoulder']], self.pose[self.nodes['RKnee']])
        dist5 = self.distance(self.pose[self.nodes['RShoulder']], self.pose[self.nodes['RHip']])
        dist6 = self.distance(self.pose[self.nodes['RHip']], self.pose[self.nodes['RKnee']])

        div1 = dist1/(dist2+dist3)
        div2 = dist4/(dist5+dist6)
        # print('[SG]', self.id, ang1, ang2, ang3, div1, div2)

    
        if ang1 < 1.5 and (ang2 < 2.8 or ang3 < 2.8): # and (div1 < 0.95 or div2 < 0.95):
            self.feature.append(3)
            return True
        else:
            return False

    def sgeorge2(self):
        ang1 = self.angle(self.pose[self.nodes['LElbow']] - self.pose[self.nodes['LShoulder']], 
                          self.pose[self.nodes['LHip']] - self.pose[self.nodes['LShoulder']])

        ang2 = self.angle(self.pose[self.nodes['RElbow']] - self.pose[self.nodes['RShoulder']], 
                          self.pose[self.nodes['RHip']] - self.pose[self.nodes['RShoulder']])

        ang3 = self.angle(self.pose[self.nodes['LHip']] - self.pose[self.nodes['LKnee']], 
                          self.pose[self.nodes['LFoot']] - self.pose[self.nodes['LKnee']])
        ang4 = self.angle(self.pose[self.nodes['RHip']] - self.pose[self.nodes['RKnee']], 
                          self.pose[self.nodes['RFoot']] - self.pose[self.nodes['RKnee']])

        if ((ang1 > math.pi/2 and ang2 < math.pi/4) or (ang2 > math.pi/2 and ang1 < math.pi/4)) and (ang3 < 2.8 or ang4 < 2.8):
            self.feature.append(3)
            return True
        else:
            return False



    def compute_features(self):
        c = self.chinchin2()
        h = self.habitant()
        d = self.diable2()
        s = self.sgeorge2()

        if not c and not h and not d and not s:
            self.feature.append(4)

        # self.feature = self.feature[-self.feature_buffer:]


class People():
    def __init__(self):
        self.people = []
        self.nop = 0
        self.latest_id = 0
        
    def index_by_id(self, id):
        for i in range(self.nop):
            if self.people[i].id == id:
                return i
        return -1


    def add_person(self, pose, box, active=False):
        person = Person()
        person.init(pose, box)
        person.id = self.latest_id + 1
        person.active = active
        self.people.append(person)
        self.latest_id += 1
        self.nop += 1


    def distance(self, p1, p2):
        return np.linalg.norm(p1-p2)

    def pdistance(self, person1, person2):
        p1 = person1.position
        p2 = person2.position
        return self.distance(p1, p2)

    def nearest_person(self, person, people):
        if self.nop == 0:
            return 1000., -1

        dists = []
        for i in range(self.nop):
            dists.append(self.pdistance(person, people[i]))
        i = np.argmin(np.array(dists))
        return dists[i], self.people[i].id
        

    def track(self, persons, smallest=55.):
        list_of_available_people = []
        for person in persons:
            dist, id = self.nearest_person(person, self.people)
            if dist <= smallest:
                self.people[self.index_by_id(id)].update(person)
                list_of_available_people.append(id)
            else:
                person.id = self.latest_id +1
                self.latest_id += 1
                self.nop += 1
                list_of_available_people.append(person.id)
                self.people.append(person)
        for person in self.people:
            if person.id not in list_of_available_people:
                # del self.people[self.index_by_id(id)]
                self.remove_person(person.id)
                


    def compute_features(self):
        for i in range(self.nop):
            self.people[i].compute_features()
        # self.people[0].compute_features()


    def remove_person(self, id):
        del self.people[self.index_by_id(id)]
        self.nop -= 1

    

                






