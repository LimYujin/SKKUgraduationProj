import RPi.GPIO as GPIO
import time


TRIG = 15
ECHO = 14
BUTTON = 20
LED_BLUE = 13

leg_dist = 100

def estimateDist():
      GPIO.output(TRIG, GPIO.LOW)  # 10m/s 동안 초음파를 쏴야함
      time.sleep(0.00001)                # 기초단위가 1초라서 10us는 10의 마이너스 5승으로 처리
      GPIO.output(TRIG, GPIO.HIGH)

      #시간측정
      while GPIO.input(ECHO) == 0:  # 펄스 발생(초음파 전송이 끝나는 시간을 start에 저장)
         start = time.time()
      while GPIO.input(ECHO) == 1:  # 펄스 돌아옴(초음파 수신이 완료될때까지의 시간을 stop에 저장)
         stop = time.time()

      rtTotime = stop - start   # 리턴 투 타임 = (end시간 - start시간)

      # 거리 = 시간 * 속력
      # 이때 소리의  속력은 340m/s인데 cm로 단위를 바꿔줘야함=> 34000 cm/s
      # 그리고 340m/s 는 왕복속도라서 편도로 봐야하니 나누기 2를 해줘야함
      distance = rtTotime * ( 34000 / 2 )
      return distance

def buttonSetting(self):
    print("Setting button is detected.\n")
    leg_dist = estimateDist()
    print("Setting done: %.2f cm" %leg_dist)
    

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LED_BLUE, GPIO.OUT)

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=buttonSetting)

cnt = 0
try:
    while True:
        distance = estimateDist()
        print("distance: %.2f cm" %distance)

        if(distance > leg_dist + 20):
            cnt = cnt + 1
        else:
            cnt = 0

        if(cnt > 10):
            GPIO.output(LED_BLUE, GPIO.HIGH)
        else:
            GPIO.output(LED_BLUE, GPIO.LOW)

        time.sleep(1)
        '''
      #구형파 발생
      GPIO.output(TRIG, GPIO.LOW)  # 10m/s 동안 초음파를 쏴야함
      time.sleep(0.00001)                # 기초단위가 1초라서 10us는 10의 마이너스 5승으로 처리

      GPIO.output(TRIG, GPIO.HIGH)

      #시간측정
      while GPIO.input(ECHO) == 0:  # 펄스 발생(초음파 전송이 끝나는 시간을 start에 저장)
         start = time.time()
      while GPIO.input(ECHO) == 1:  # 펄스 돌아옴(초음파 수신이 완료될때까지의 시간을 stop에 저장)
         stop = time.time()

      rtTotime = stop - start   # 리턴 투 타임 = (end시간 - start시간)

      # 거리 = 시간 * 속력
      # 이때 소리의  속력은 340m/s인데 cm로 단위를 바꿔줘야함=> 34000 cm/s
      # 그리고 340m/s 는 왕복속도라서 편도로 봐야하니 나누기 2를 해줘야함
      distance = rtTotime * ( 34000 / 2 )
      print("distance : %.2f cm" %distance) # 거리를 출력
      time.sleep(1)  # 1초마다 받아옴
      '''

except KeyboardInterrupt:
   GPIO.cleanup()
