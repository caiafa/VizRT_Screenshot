import configparser

config = configparser.ConfigParser()
config.read('config.ini')

popup_list_path = config['popup']['filepath']
prefix = config['viz paths']['prefix']
preview_server = config['preview server']['ip']
backgrounds = config['resources']['backgrounds']
hd_offset = config['popup']['hd_offset']
