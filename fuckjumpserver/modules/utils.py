#__author__:"jcm"
import yaml
try:
    from yaml import Cliader as Loader,CDumper as Dumper
except ImportError:
    from yaml import Loader,Dumper

def print_err(msg,quit=False):
    output="\033[31;1mError:%s\033[0m"%msg
    if quit:
        exit(output)
    else:
        print(output)
#处理yaml文件
def yaml_parser(yml_filename):
    '''
    load yaml file and return
    :param yml_filename:
    :return:
    '''
    #yml_filename = "%s/%s.yml" % (settings.StateFileBaseDir,yml_filename)
    try:
        #打开yaml文件
        yaml_file = open(yml_filename,'r')
        #将yaml文件中的信息导出，导出文件为字典格式
        data = yaml.load(yaml_file,Loader=yaml.FullLoader)
        return data
    except Exception as e:
        print_err(e)