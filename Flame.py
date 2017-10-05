#This code is about flame sensor.
#We use flame sensor and mcp3008 ADC.
#We have got many helps from http://blog.naver.com/roboholic84/220367321777
#We use spidev module.
#SPI should be enable before running this code.
#And we also use MySQL, to save sensing log.
#DB ID is Flame.
#This code will be run background.
#Team Be-Care, by KimJunyeong.

import time
import MySQLdb
import spidev

def Flame_read(channel):
        '''Getting sensor value from mcp3008 ADC'''
        data = spi.xfer2([1, (8 + channel) << 4, 0]) #SPI transaction
        flame_power = ((data[1]&3) << 8) + data[2]
        return flame_power

#main
spi = spidev.SpiDev()
spi.open(0,0)   #open (bus, device)
detected = 0    #Is flame on now?

try:
        db=MySQLdb.connect(host='localhost', user='Flame',\
                                passwd='flame', db='Be_Care')
        with db:
                cur=db.cursor()
        while True:
                flame = Flame_read(0)
                if flame > 10 and detected == 0:        #flame detected
                        time_string=time.strftime("%H:%M:%S", time.localtime())
                        cur.execute("INSERT INTO Flame(Flame, Time) VALUES(%s, %s);", (1, time_string))
                        db.commit()
                        detected = 1
                #elif flame > 10 and detected == 1:
                #       time_string=time.strftime("%H:%M:%S", time.localtime())
                #       cur.execute("UPDATE Flame SET Time=%s WHERE (SELECT * FROM FLAME ORDER BY Time DESC LIMIT 1)", time_string)
                #       db.commit()
                elif flame <= 10 and detected == 1:
                        detected = 0
                #print (flame, detected)
                time.sleep(1)
except Exception as error:
        print error
        db.close()
