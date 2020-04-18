import json
import os

configurationFile = 'config.json'
templateFile = 'docker-compose.template'

def replaceStrings(configfile, tag, config):
  print('Replace tag' + tag + ' in file ' + configfile)

  with open(configfile, 'r') as file :
    filedata = file.read()

  filedata = filedata.replace(tag, config)

  with open(configfile, 'w') as file:
    file.write(filedata)

def pullImages(image):
  print('Pull image: ' + image)
  os.system('docker pull ' + image)

def copyConfigFiles(source,destination):
  print('Copy file' + source + ' to ' + destination)
  os.system('cp ' + source + ' ' + destination)

def createDir(x):
  print ('Create directory: ' + x)

  if not os.path.exists('../'+ x):
    os.makedirs('../'+ x)


with open(configurationFile) as json_file:

    data = json.load(json_file)

    for p in data['containerConfiguration']:

        print('PyDocker Configuration Script')
        print('')
        print('1) app name: ' + p['appName'])
        print('2) project docker name: ' + p['projectName'])
        print('3) container ip address: ' + p['appIp'])
        print('4) network name: ' + p['network'])
        print('5) app tcp ports: \n\n' + 'PhP App: ' + p['appPortWP'] + '\nDatabase: ' + p['appPortWP'] + '\nPhpMyAdmin: ' + p['appPortPhpMyAdmin'] + '\n')
        print('')

        # 1) Create a app structure directories 
        print('** 1 ** Create a directories...')
        createDir(str(p['appVolume']))
        createDir(str(p['phpMyAdminVolume']))
        createDir(str(p['dbVolume']))
        createDir(str(p['dbVolume']+'/initdb.d'))
        createDir(str(p['appPhpIniVolume']))
        print('')

        # 2) Copy a configuration files
        print('** 2 ** Copy a configuration files...')
        copyConfigFiles('configs_examples/php.ini','../etc/')
        print('')

        # 3) Pull a Docker Images
        print('** 3 ** Pull a docker images used from application ...')
        pullImages(str(p['phpAppImage']))
        pullImages(str(p['dbAppImage']))
        pullImages(str(p['phpMyAdminImage']))
        print('')

        #4) Build a Docker-Compose File
        print('** 4 ** Build a Docker Compose File ...')
        copyConfigFiles('docker-compose.template','docker-compose.yml')
        replaceStrings('docker-compose.yml', '[[appName]]', str(p['appName']))
        replaceStrings('docker-compose.yml', '[[appPortWP]]', str(p['appPortWP']))
        replaceStrings('docker-compose.yml', '[[appPortDb]]', str(p['appPortDb']))
        replaceStrings('docker-compose.yml', '[[appPortPhpMyAdmin]]', str(p['appPortPhpMyAdmin']))
        replaceStrings('docker-compose.yml', '[[appIp]]', str(p['appIp']))
        replaceStrings('docker-compose.yml', '[[network]]', str(p['network']))
        replaceStrings('docker-compose.yml', '[[phpAppImage]]', str(p['phpAppImage']))
        replaceStrings('docker-compose.yml', '[[dbAppImage]]', str(p['dbAppImage']))
        replaceStrings('docker-compose.yml', '[[phpMyAdminImage]]', str(p['phpMyAdminImage']))
        replaceStrings('docker-compose.yml', '[[dbRootPassword]]', str(p['dbRootPassword']))
        replaceStrings('docker-compose.yml', '[[dbPassword]]', str(p['dbPassword']))
        replaceStrings('docker-compose.yml', '[[dbName]]', str(p['dbName']))
        replaceStrings('docker-compose.yml', '[[dbUser]]', str(p['dbUser']))
        replaceStrings('docker-compose.yml', '[[appVolume]]', str(p['appVolume']))
        replaceStrings('docker-compose.yml', '[[phpMyAdminVolume]]', str(p['phpMyAdminVolume']))
        replaceStrings('docker-compose.yml', '[[appPhpIniVolume]]', str(p['appPhpIniVolume']))
        replaceStrings('docker-compose.yml', '[[dbVolume]]', str(p['dbVolume']))
        print('')

        #5) Build Container Start and Stop scripts
        print('** 5 ** Build a Start and Stop script')
        copyConfigFiles('start.template','start.sh')
        replaceStrings('start.sh', '[[projectName]]', str(p['projectName']))
        copyConfigFiles('stop.template','stop.sh')
        replaceStrings('stop.sh', '[[projectName]]', str(p['projectName']))
        print('')

        # 6) Copy configuration files
        print('** 6 ** Copy configuration files to hot folder')
        copyConfigFiles('start.sh','../start.sh')
        copyConfigFiles('stop.sh','../stop.sh')
        copyConfigFiles('docker-compose.yml','../docker-compose.yml')
        print('')

        # 7) Remove temp files
        print('** 7 ** Finish a configuration')
        os.system('rm -f start.sh')
        os.system('rm -f stop.sh')
        os.system('rm -f docker-compose.yml')


        # 8) Finish
        print('** 8 ** Finish a configuration')
        os.system('chmod +x ../start.sh')
        os.system('chmod +x ../stop.sh')

        if str(p['autoStart'] == "yes"):
          os.system('../start.sh')
          os.system('docker-compose ps')
        















