from phue import Bridge
import argparse
import time, os

# Type in your path to .python_hue file
KEY_FILE=".python_hue" 

# Type in your Hue Bridge IP Address
BRIDGE="x.x.x.x"

print KEY_FILE

b = Bridge(BRIDGE, config_file_path=KEY_FILE)
b.connect()
result = b.get_api()




parser = argparse.ArgumentParser(description='Blinks by type and returns to previous condition.')

parser.add_argument('-l', '--lights', help='delimited list input', type=str)
parser.add_argument('-t', '--type' , help='notification type [ie. alert, note, done, etc..]', type=str)
parser.add_argument('-c', '--count', help='delimited list input', type=int)
args = parser.parse_args()

lights = [item for item in args.lights.split(',')]
type = args.type
blinks = args.count

tgap=20

notifications = {
'alert':[0,255,255],
'done' :[30000,255,255],
'note' :[45000,255,255]
}



def rState(light):
    rhue = b.get_light(light)['state']['hue']
    rsat = b.get_light(light)['state']['sat']
    rbri = b.get_light(light)['state']['bri']
    result = {}
    result['hue']=rhue
    result['sat']=rsat
    result['bri']=rbri
    #print  result
    return result


def nSend(lights,typein):
    type=notifications[typein]
    rLights = {}
    for light in lights:
        rLights[light]=rState(light)
    new = {'hue':type[0], 'sat':type[1], 'bri':type[2]}
    b.set_light(lights, new)
    time.sleep(tgap/10)
    for blink in range(blinks):
        b.set_light(lights, {'bri':50, 'transitiontime':tgap})
        time.sleep(tgap/10)
        b.set_light(lights, {'bri':255, 'transitiontime':tgap})
        time.sleep(tgap/10)
    time.sleep(tgap/10)
    for light in lights:
        b.set_light(light,rLights[light])
    return True

nSend(lights,type)
