#include <webots/robot.h>
#include <webots/speaker.h>
#include <webots/emitter.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define BIG_TIME_STEP 3000
#define SMALL_TIME_STEP 640


char colors[5][4] = {"red", "blu", "gre", "yel", "pur"};
char numbers[9][2] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};

int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();
  srand(time(NULL));
  WbDeviceTag speaker = wb_robot_get_device("speaker");
  WbDeviceTag emitter = wb_robot_get_device("emitter");
  
  while (wb_robot_step(BIG_TIME_STEP) != -1) {
    // char* color = colors[rand() % 5];
    // char* number = numbers[rand() % 9];
    char* color = colors[0];
    char* number = numbers[4];

    wb_speaker_speak(speaker, color, 1.0);
    wb_robot_step(SMALL_TIME_STEP);
    wb_speaker_speak(speaker, number, 1.0);
    wb_robot_step(2 * SMALL_TIME_STEP);

    wb_emitter_send(emitter, color, 4);
    wb_emitter_send(emitter, number, 2);
  }

  wb_robot_cleanup();
  return 0;
}
