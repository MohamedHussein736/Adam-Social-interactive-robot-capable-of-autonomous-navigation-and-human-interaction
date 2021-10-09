                                                                                                                                        #Import Computer Vision                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
import face_recognition
import cv2
from PIL import Image, ImageDraw
import scipy.misc

#ros lib
import rospy
from std_msgs.msg import Int16,Int32, Int64, Float32, String, Header, UInt64

#Time 
import time
################################################################################
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
string=""

################################################################################
###class image1#######
class face(object):
        
    	def __init__(self):
	        rospy.Subscriber('num1',String,self._perName1)	       
                rospy.Subscriber('num2',String,self._clear)
                self.data =''
                self._c=0
                self._name =["noname","noname","noname","noname","noname"]
        #callback funcation
        def _perName1(self, personName1):
    		    self._name[self._c] = personName1.data
                    rospy.loginfo("1-{}".format(personName1.data))
                    rospy.loginfo("z={}".format(self._c))
        def _clear(self, clear):
        		self.data = clear.data
                    #rospy.loginfo("CLEAR: {}".format(clear.data))

################################################################################
###Funcation Image#######
def image():
    ##Initialize some variables
    x=0
    y=0
    m =False
    z=0
    while True:
        t=True
        f=False
        rospy.loginfo("loop.{}".format(m))
        if launchpad.data == 'clear':
            clear_image = face_recognition.load_image_file("0.jpg")
            scipy.misc.imsave("./{}.jpg".format(1), clear_image)
            scipy.misc.imsave("./{}.jpg".format(2), clear_image)
            scipy.misc.imsave("./{}.jpg".format(3), clear_image)
            scipy.misc.imsave("./{}.jpg".format(4), clear_image)
            launchpad.data ='no'
            x=0 
            y=0
            z=0
            #Print that image x is saved
            rospy.loginfo("clear done!")         
            ##if unknown face is detected
        if x != 0:
            ##Initialize some variables
            z = x-1
            launchpad._c=z
            launchpad._name[z] ="noname"

            ##display unknown face Image 
            cv2.imshow('Video',frame[top:bottom, left:right])
            cv2.waitKey(1000)

            ##Ask unknown face about his/her name        
            rospy.loginfo("who are you MR.Unkown{}?".format(z))

            #Wait until get The name from ros topic
            while(launchpad._name[z] == "noname"):
                launchpad._name[z] ="noname"
                time.sleep(0.1) 

            ##Print Name
            rospy.loginfo("{}".format(launchpad._name[z]))

            ##destroy Image window
            cv2.destroyAllWindows()
            ###############################################################
        
        ###################################################################
        #Load image zero that will be used in error encoding
        zero_image = face_recognition.load_image_file("0.jpg")

        #Load image one and encode the face from the image
        one_image = face_recognition.load_image_file("1.jpg")
        try:
            one_face_encoding = face_recognition.face_encodings(one_image)[0]
        except:
            one_face_encoding = face_recognition.face_encodings(zero_image)[0]
            ##if face not clear in the Image retake the image
            if z > 0:
                #pass
                x-=1
            else:
                pass
        
        #Load image two and encode the face from the image
        two_image = face_recognition.load_image_file("2.jpg")
        try:
            two_face_encoding = face_recognition.face_encodings(two_image)[0]
        except:
            two_face_encoding = face_recognition.face_encodings(zero_image)[0]
            if z > 0:
                #pass
                x-=1
            else:
                pass

        #Load image three and encode the face from the image
        three_image = face_recognition.load_image_file("3.jpg")
        try:
            three_face_encoding = face_recognition.face_encodings(three_image)[0]
        except:
            three_face_encoding = face_recognition.face_encodings(zero_image)[0]
            if z > 0:
                #pass
                x-=1
            else:
                pass

        #Load image four and encode the face from the image
        four_image = face_recognition.load_image_file("4.jpg")
        try:
            four_face_encoding = face_recognition.face_encodings(four_image)[0]
        except:
            four_face_encoding = face_recognition.face_encodings(zero_image)[0]
            if z > 0:
                #pass
                x-=1
            else:
                pass

        ###################################################################
        # Create arrays of known faces encodings 
        known_face_encodings = [
            one_face_encoding,
            two_face_encoding,
            three_face_encoding,
            four_face_encoding
        ]
        # Create arrays of known faces names        
        known_face_names = [
            launchpad._name[0],
            launchpad._name[1],
            launchpad._name[2],
            launchpad._name[3]
        ]
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        launchpad._name1 = string
        ###################################################################
        ##loop if there isn't any unknown faces or database is completed
        while f == False:
            
            launchpad._name1 = string
            
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            #save video frames
            #cv2.imwrite("./frames/frame.jpg",frame)

            ##############################################################
            ##Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []

                #loop on all detected faces in the frame
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    #display face name    
                    face_names.append(name)
            #for decode the faces every two frames to save time
            process_this_frame = not process_this_frame

            ##############################################################
            ##Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):

                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # if the face is known 
                if True in matches:
                    rospy.loginfo("old")

                # if the face is unknown and database still have space 
                elif x < 5 and name=="Unknown":
                    y+=1
                    ##save Face image in the database
                    face_image = frame[top:bottom, left:right]
                    image2 = Image.fromarray(face_image)
                    scipy.misc.imsave("./{}.jpg".format(x+1), image2)
                    #Print that image x is saved
                    rospy.loginfo("save.{}".format(y))
                    t = False
                    #extract face height & width
                    #height, width = face_image.shape[:2]

                ##database is complete
                else:
                    rospy.loginfo("full images")

                if launchpad.data == "clear":
                    f= True
                else:
                    pass
                ##############################################################
                ## Draw a box around the face

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                #rospy.loginfo(name) 
            
            # Display the resulting image
            cv2.imshow('Video', frame)
        
            rospy.loginfo("x={}".format(x))
            rospy.loginfo("y={}".format(y))

            #Capture Frame when Press 's'
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite("./test2/mh6.jpg",frame)

            ##if unkown face is detected and database not complete break the loop to relearn
            if t == False:
                x+=1
                f= True

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                m=True
                break
        ##if 'q' is pressed break the loop   
        if m==True:
            break
        ###################################################################

if __name__ =='__main__':
    ##create ROS Node
    rospy.init_node('video',anonymous=True)
    #create object 
    launchpad = face()
    #call the face detection funcation
    image()	
    #release the video 
    video_capture.release()
    #destroy all tabs 
    cv2.destroyAllWindows()

