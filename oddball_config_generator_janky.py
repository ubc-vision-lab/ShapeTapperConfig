import random
import sys
import os
import re
import math
import shape_utils as su

#required for functions found online
import struct
import imghdr


# ODDBALL CONFIG GENERATOR
# uses blake shapes only.

#things you might want to change
# other variable initializations. Should set so they can be changed/configured.
feedback = 0
practice = 1
block_pass_percent = 0
block_fb = 1
timeout = 60
total1 = total2 = total3 = timeout
onset = 1
number_of_angles = 18 #number of angles, should divide 360 evenly

safety_margin_1 = 40
safety_margin_2 = 40
safety_margin_3 = 40

#delimiter
delimiter = ","

blake_or_simple = 0 # this sets the variable values
# 0 = blake
# 1 = simple

if(blake_or_simple == 0): # blake
    image_directory = './blake_images/'
    safety_margins = [40]
    vary_size = 0
elif(blake_or_simple == 1): # simple
    image_directory = './simple_images/'
    safety_margins = [30,40,50]
    vary_size = 1

# please don't read this it's terrible and done in a couple of hours
def main():
    if(len(sys.argv) == 3):
        num_blocks = int(sys.argv[1])
        num_trials = int(sys.argv[2])
    else:
        num_blocks = 9
        num_trials = 75

    image_files = su.get_pngs(image_directory)

    for block in range(0,num_blocks):
        for trial_num in range(0,num_trials):
            #figure out which images to use first
            image_1 = image_files[random.randrange(0,len(image_files))]
            image_2 = image_files[random.randrange(0,len(image_files))]
            while image_1 == image_2:
                image_2 = image_files[random.randrange(0,len(image_files))]
            #figure out positions
            # get image sizes
            # images are scaled to a percentage of the height, along the images' diagonal
            img_1_width, img_1_height = su.get_image_size(image_directory + image_1)
            img_1_diag = math.hypot(img_1_width, img_1_height)
            safety_margin_1 = su.get_scaling(vary_size,safety_margins)
            img_1_scale = img_1_diag*su.screen_height/float(safety_margin_1)/100
            img_1_width /= img_1_scale
            img_1_height /= img_1_scale
            img_1_diag = float(safety_margin_1)*su.screen_height/100
            #print("img1scale: " + str(img_1_scale))
            #print("img_1_width: " + str(img_1_width) + "; img_1_height: " + str(img_1_height) + "; img_1_diag: " + str(img_1_diag))

            if(vary_size):
                same_sizes = random.randint(0,1)
                # coin toss to see if the first image will be the same as the others
                safety_margins_trial = list(safety_margins)
                if(same_sizes): # 50% chance to match at least one
                    safety_margin_2 = safety_margin_1
                else:
                    safety_margins_trial.remove(safety_margin_1)
                    safety_margin_2 = su.get_scaling(vary_size,safety_margins_trial)
                
                same_distractor_size = random.randint(0,1)
                if(same_distractor_size):
                    safety_margin_3 = safety_margin_2
                else:
                    safety_margins_trial.remove(safety_margin_2)
                    safety_margin_3 = su.get_scaling(vary_size,safety_margins_trial)
            else:
                safety_margin_2 = safety_margin_1
                safety_margin_3 = safety_margin_1

            img_2_width, img_2_height = su.get_image_size(image_directory + image_2)
            img_2_diag = math.hypot(img_2_width, img_2_height)
            
            img_2_scale = img_2_diag*su.screen_height/float(safety_margin_2)/100
            img_2_width /= img_2_scale
            img_2_height /= img_2_scale
            img_2_diag = float(safety_margin_2)*su.screen_height/100
            #print("img2scale: " + str(img_2_scale))
            #print("img_2_width: " + str(img_2_width) + "; img_2_height: " + str(img_2_height) + "; img_2_diag: " + str(img_2_diag))

            img_3_width, img_3_height = su.get_image_size(image_directory + image_2)
            img_3_diag = math.hypot(img_3_width, img_3_height)
            img_3_scale = img_3_diag*su.screen_height/float(safety_margin_3)/100
            img_3_width /= img_3_scale
            img_3_height /= img_3_scale
            img_3_diag = float(safety_margin_3)*su.screen_height/100
            #print("img3scale: " + str(img_3_scale))
            #print("img_3_width: " + str(img_3_width) + "; img_3_height: " + str(img_3_height) + "; img_3_diag: " + str(img_3_diag))

            pos_img_1_x = su.get_random_x(round(img_1_diag))
            pos_img_1_y = su.get_random_y(round(img_1_diag))
            pos_img_2_x = pos_img_1_x
            pos_img_2_y = pos_img_1_y
            pos_img_3_x = pos_img_1_x
            pos_img_3_y = pos_img_1_y

            #potential for infinite loop depending on image sizes. for 1080p shouldn't be a problem.
            while (math.hypot(pos_img_1_x-pos_img_2_x,pos_img_1_y-pos_img_2_y) < (img_1_diag + img_2_diag)/2
                or math.hypot(pos_img_1_x-pos_img_3_x,pos_img_1_y-pos_img_3_y) < (img_1_diag + img_3_diag)/2
                or math.hypot(pos_img_2_x-pos_img_3_x,pos_img_2_y-pos_img_3_y) < (img_2_diag + img_3_diag)/2
                ): #while the image distances overlap
                pos_img_1_x = su.get_random_x(round(img_1_diag))
                pos_img_1_y = su.get_random_y(round(img_1_diag))
                pos_img_2_x = su.get_random_x(round(img_2_diag))
                pos_img_2_y = su.get_random_y(round(img_2_diag))
                pos_img_3_x = su.get_random_x(round(img_3_diag))
                pos_img_3_y = su.get_random_y(round(img_3_diag))

            #convert positions into percentages (wait what this might mean overlap)
            pos_img_1_x = int(round(pos_img_1_x * float(100)/su.get_margin_width(img_1_diag)))
            pos_img_1_y = int(round(pos_img_1_y * float(100)/su.get_margin_height(img_1_diag)))
            pos_img_2_x = int(round(pos_img_2_x * float(100)/su.get_margin_width(img_2_diag)))
            pos_img_2_y = int(round(pos_img_2_y * float(100)/su.get_margin_height(img_2_diag)))
            pos_img_3_x = int(round(pos_img_3_x * float(100)/su.get_margin_width(img_3_diag)))
            pos_img_3_y = int(round(pos_img_3_y * float(100)/su.get_margin_height(img_3_diag)))

            #identifier
            trial_config = str(block+1) + delimiter
            trial_config += str(trial_num+1) + delimiter

            #trial specific
            trial_config += str(feedback) + delimiter

            #block level stuff
            trial_config += str(practice) + delimiter
            trial_config += str(block_pass_percent) + delimiter
            trial_config += str(block_fb) + delimiter

            #trial-specific stuff
            trial_config += str(timeout) + delimiter
            trial_config += delimiter
            trial_config += delimiter * 5 # janky stuff to skip dynamic masks - not used in oddball
            trial_config += str(1) + delimiter # this is number of replays of trial within timeout, but again, not used in oddball
            trial_config += str(pos_img_1_x) + delimiter
            trial_config += str(pos_img_1_y) + delimiter
            trial_config += str(onset) + delimiter
            
            #image 1
            trial_config += (image_1.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * random.randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_1) + delimiter
            trial_config += str(1) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 2
            trial_config += (image_2.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * random.randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_2) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            trial_config += str(0) + delimiter # not used in oddball image_off

            #image 3
            trial_config += (image_2.split('.'))[0] + delimiter
            trial_config += str(number_of_angles * random.randrange(0,360/number_of_angles)) + delimiter
            trial_config += str(safety_margin_3) + delimiter
            trial_config += str(0) + delimiter # we're gonna assume target 1 will always be the oddball since, well, we're scripting here
            trial_config += str(0) + delimiter # dyn_mask_flag not used
            trial_config += str(total1) + delimiter
            trial_config += str(0) + delimiter # not used in oddball image_on
            # no image_off for image 3

            #bonus oddball config stuff
            trial_config += str(1) + delimiter #oddball_flag
            trial_config += str(pos_img_2_x) + delimiter
            trial_config += str(pos_img_2_y) + delimiter
            trial_config += str(pos_img_3_x) + delimiter
            trial_config += str(pos_img_3_y)
            print(trial_config)
    return

if __name__ == "__main__":
    main()
