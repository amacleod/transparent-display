#include <avr/io.h>
#include <SPI.h>

// Pins on the Seeeduino to pins on the Crystalfontz display:
// Seeeduino  Crystalfontz   Wire Color  Function
//  D8         08 (CS)       Purple      Component Select for SPI
//  D9         10 (RST)      Grey        Reset Peripheral
//  D11        01            Blue        Serial Data Out
//  D13        00            Green       Serial Clock
//  A0         09 (D/C)      Brown       Data / Command Selector

#define CS_LOW (PORTB &= ~(0x01))     //pin #8  - Chip Enable Signal
#define CS_HIGH (PORTB |= (0x01))     //pin #8  - Chip Enable Signal
#define RESET_LOW (PORTB &= ~(0x02))  //pin #10 - Reset
#define RESET_HIGH (PORTB |= (0x02))  //pin #10 - Reset

#define DC_LOW (PORTC &= ~(0x01))     //pin #9  - Data/Instruction
#define DC_HIGH (PORTC |= (0x01))     //pin #9  - Data/Instruction
#define WR_LOW (PORTC &= ~(0x02))     //pin #10 - Write
#define WR_HIGH (PORTC |= (0x02))     //pin #10 - Write
#define RD_LOW (PORTC &= ~(0x04))     //pin #11 - Read
#define RD_HIGH (PORTC |= (0x04))     //pin #11 - Read
#define DEBUG_LOW (PORTC &= ~(0x08))  //pin #12 - Debug
#define DEBUG_HIGH (PORTC |= (0x08))  //pin #12 - Debug

#define COMMAND_MODE DC_LOW
#define DATA_MODE DC_HIGH

#define MAX_BRIGHT (0x8F)

/**
 * Write a one-byte command to the display, by pulling the
 * "command/data" pin low (command mode) and the chip select
 * pin low before writing that byte to the SPI bus.
 */
void writeCommand(uint8_t command) {
  COMMAND_MODE;
  CS_LOW;
  SPI.transfer(command);
  CS_HIGH;
}

/**
 * Write one byte of data to the display, by pulling the
 * "command/data" pin high (data mode) and the chip select pin high
 * before writing the byte to the SPI bus.
 */
void writeData(uint8_t data) {
  DATA_MODE;
  CS_LOW;
  SPI.transfer(data);
  CS_HIGH;
}

//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  Instruction Setting
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void Set_Start_Column(uint8_t d) {
  writeCommand(0x00 + d % 16);  // Set Lower Column Start Address for Page Addressing Mode
                                //   Default => 0x00
  writeCommand(0x10 + d / 16);  // Set Higher Column Start Address for Page Addressing Mode
                                //   Default => 0x10
}
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void Set_Column_Address(uint8_t a, uint8_t b) {
  writeCommand(0x21);  // Set Column Address
  writeCommand(a);     //   Default => 0x00 (Column Start Address)
  writeCommand(b);     //   Default => 0x7F (Column End Address)
}
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void Set_Page_Address(uint8_t a, uint8_t b) {
  writeCommand(0x22);  // Set Page Address
  writeCommand(a);     //   Default => 0x00 (Page Start Address)
  writeCommand(b);     //   Default => 0x07 (Page End Address)
}
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void Set_Start_Page(uint8_t d) {
  writeCommand(0xB0 | d);  // Set Page Start Address for Page Addressing Mode
                           //   Default => 0xB0 (0x00)
}
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//  Show Regular Pattern (Full Screen)
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
void Fill_RAM(uint8_t Data) {
  uint8_t
    i;
  uint8_t
    j;

  for (i = 0; i < 8; i++) {
    Set_Start_Page(i);
    Set_Start_Column(0x00);

    for (j = 0; j < 128; j++) {
      writeData(Data);
    }
  }
}

#define XLevelL 0x00
#define XLevelH 0x10
#define XLevel ((XLevelH & 0x0F) * 16 + XLevelL)
#define Brightness 0xBF

void OLED_Init() {
  //The CFA10105 has a power-on reset circuit,
  //you can use the following code if you are using GPIO for reset
  RESET_LOW;
  delay(1);
  RESET_HIGH;
  delay(120);

  writeCommand(0xFD);  // Set Command Lock
  writeCommand(0X12);  //   Default => 0x12
                       //     0x12 => Driver IC interface is unlocked from entering command.
                       //     0x16 => All Commands are locked except 0xFD.

  writeCommand(0XAE);  // Set Display On/Off
                       //   Default => 0xAE
                       //     0xAE => Display Off
                       //     0xAF => Display On


  writeCommand(0xD5);  // Set Display Clock Divide Ratio / Oscillator Frequency
                       //  writeCommand(0XA0);	// Set Clock as 116 Frames/Sec
  writeCommand(0X30);  // Set Clock as 116 Frames/Sec
                       //   Default => 0x70
                       //     D[3:0] => Display Clock Divider
                       //     D[7:4] => Oscillator Frequency

  writeCommand(0xA8);  // Set Multiplex Ratio
  writeCommand(0X37);  //   Default => 0x3F (1/56 Duty)

  writeCommand(0xD3);  // Set Display Offset
  writeCommand(0X08);  //   Default => 0x00

  writeCommand(0x40);  // Set Mapping RAM Display Start Line (0x00~0x3F)
                       //   Default => 0x40 (0x00)

  //writeCommand(0xD8);	// Set Low Power Display Mode (0x04/0x05)
  //writeCommand(0x05);	//   Default => 0x04 (Normal Power Mode)

  writeCommand(0xA1);  // Set SEG/Column Mapping (0xA0/0xA1)
                       //   Default => 0xA0
                       //     0xA0 => Column Address 0 Mapped to SEG0
                       //     0xA1 => Column Address 0 Mapped to SEG127

  writeCommand(0xC8);  // Set COM/Row Scan Direction (0xC0/0xC8)
                       //   Default => 0xC0
                       //     0xC0 => Scan from COM0 to 63
                       //     0xC8 => Scan from COM63 to 0

  writeCommand(0xDA);  // Set COM Pins Hardware Configuration
  writeCommand(0x12);  //   Default => 0x12
                       //     Alternative COM Pin Configuration
                       //     Disable COM Left/Right Re-Map

  writeCommand(0x81);  // Set SEG Output Current
  writeCommand(0x8F);  // Set Contrast Control for Bank 0

  writeCommand(0xD9);  // Set Pre-Charge as 2 Clocks & Discharge as 5 Clocks
  writeCommand(0x25);  //   Default => 0x22 (2 Display Clocks [Phase 2] / 2 Display Clocks [Phase 1])
                       //     D[3:0] => Phase 1 Period in 1~15 Display Clocks
                       //     D[7:4] => Phase 2 Period in 1~15 Display Clocks

  writeCommand(0xDB);  // Set VCOMH Deselect Level
  writeCommand(0x34);  //   Default => 0x34 (0.78*VCC)

  writeCommand(0xA4);  // Set Entire Display On / Off
                       //   Default => 0xA4
                       //     0xA4 => Normal Display
                       //     0xA5 => Entire Display On

  writeCommand(0xA6);  // Set Inverse Display On/Off
                       //   Default => 0xA6
                       //     0xA6 => Normal Display
                       //     0xA7 => Inverse Display On

  Fill_RAM(0x00);  // Clear Screen

  writeCommand(0XAF);  // Display On (0xAE/0xAF)
}

/**
 * Given an array of bytes, each of which represents a strip of 8 pixels,
 * write the whole image to the display, one byte at a time.
 */
void displayImage(const uint8_t image[896]) {
  // Pages 0 through 6 constitute the visible portion of the screen, the upper 56 rows of pixels.
  for (uint8_t y = 0; y < 7; y++) {
    // Set the starting page and column
    Set_Start_Page(y);
    Set_Start_Column(0x00);
    for (uint8_t x = 0; x < 128; x++) {
      writeData(image[(y * 128) + x]);
    }
  }
  //Clear the last page so stray pixels do not show in getter area.
  Set_Start_Page(7);
  Set_Start_Column(0x00);
  for (uint8_t x = 0; x < 128; x++) {
    writeData(0x00);
  }
}

void setup() {
  // Set up port directions: for each bit, 1=output and 0=input.
  DDRC |= 0x01; // Analog pin 0 output, all others remain as they were.
  DDRB |= 0x03; // Digital pins 8 and 9 output, all others remain as they were.

  //SPI begin transactions takes ~2.5us
  SPI.begin();
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

  //OLED_Init takes ~120ms
  OLED_Init();

  Serial.begin(115200);
  Serial.println("READY");
}

void loop() {
  // Serial.println("DEBUG hello");
  // delay(100);
  char buffer[896];
  request_image(buffer);
  displayImage(buffer);
  // Serial.println("DEBUG image displayed");
}

int request_image(char *buf) {
  Serial.println("FRAME 896");
  size_t bytes_read = Serial.readBytes(buf, 896);
  // Serial.print("DEBUG bytes_read=");
  // Serial.println(bytes_read);
  return 0;
}
