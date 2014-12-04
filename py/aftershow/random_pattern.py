import time
import random

# This import gives you full acess to the hardware
import hardware_controller as hc

# this is a list of all the channels you have access to
# I'm also traking the time, here so that I know when I turned a light on
# So I'm putting everything in a dict
lights = dict.fromkeys(range(0, len(hc._GPIO_PINS)), [True, time.time()])

# get a number that is about 40% the length of your gpio's
# this will be use to make sure that no more then 40% of 
# the light will be off at any one time
max_off = int(round(len(lights) * .4))

def main():
    """
    Random flashing lights
    """
    # initialize your hardware for use
    hc.initialize()
    print "Press <CTRL>-C to stop"

    # lets make sure we start with all the lights on
    hc.turn_on_lights()

    # pause for 2 second
    time.sleep(2)

    # working loop
    while True:
        # try except block to catch the <CTRL>-C to stop
        try:
            # here we just loop over the gpio pins and do something with them
            for light in lights:
                # this is where we check to see if we have any light
                # that are turned off
                # if they are off we will check the time to see if we
                # want to turn them back on yet, if we do then turn it on
                if not lights[light][0]:
                    if lights[light][1] < time.time():
                        lights[light][0] = True
                        hc.turn_on_light(light)
            
            # count the number of lights that are off 
            off = [k for (k, v) in lights.iteritems() if v.count(1) == False]

            # if less then out max count of light that we chose 
            # we can turn one off
            if len(off) < max_off:
                # pick a light at random to turn off
                choice = random.randrange(0, len(hc._GPIO_PINS))
                # if it's on then lets turn it off
                if lights[choice][0]:
                    # pick a duration for that light to be off
                    # default times are between 1/2 and secong and 1.8 seconds
                    duration = random.uniform(0.5, 1.8)

                    # store this informatin in our dict
                    lights[choice] = [False, time.time() + duration]
                    # and turn that light off then continue with the main loop
                    # and do it all over again
                    hc.turn_off_light(choice)

        except KeyboardInterrupt:
            print "\nstopped"
            # This ends and cleans up everything 
            # NOTE: if you do not pass in True
            #       this will start all over again
            #       and you will have to fight to
            #       get out of the loop
            hc.clean_up(True)
            break

if __name__ == "__main__":
    main()
