#ifndef NEWBEE_DISPLAY_WAVEGUIDE_H
#define NEWBEE_DISPLAY_WAVEGUIDE_H

#include <stdint.h>

int  nb_display_init(void);
void nb_display_commit(void);
void nb_display_set_brightness(uint8_t percent);

#endif /* NEWBEE_DISPLAY_WAVEGUIDE_H */
