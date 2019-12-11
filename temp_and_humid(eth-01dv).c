#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>



#define BCM_GPIO 8 // CS_MCP3208 6(BCM_GPIO 25)

#define SPI_CHANNEL 0
#define SPI_SPEED 1000000 // 1MHz


int read_mcp3208_adc(unsigned char adcChannel);

int main(void)
{
	int adcChannel = 0;
	int adcValue = 0;
	float tempo = 0;
	float tempoVolt = 0;
	float humi = 0;
	float humiVolt = 0;



	if (wiringPiSetupGpio() == -1)
	{
		fprintf(stdout, "Unable to start wiringPi: %s\n", strerror(errno));
		return 1;
	}

	if (wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1)
	{
		fprintf(stdout, "wiringPiSPISetup Failed: %s\n", strerror(errno));
		return 1;
	}

	pinMode(BCM_GPIO, OUTPUT);

	while (1)
	{
		adcChannel = 0;
		adcValue = read_mcp3208_adc(adcChannel);

		printf("MCP3208 IC Ch0 Value = %u\n", adcValue);
		tempoVolt = (3.25 / 4095)*adcValue;
		tempo = -66.875 + 218.75 * (tempoVolt / 3.3);
		printf("온도센서전압 : %f\n", tempoVolt);
		printf("현재온도 : %f\n\n ", tempo);

		adcChannel = 1;

		adcValue = read_mcp3208_adc(adcChannel);

		humiVolt = (3.25 / 4095)*adcValue;
		humi = -12.5 + 125 * (humiVolt / 3.3);
		printf("\nMCP3208 IC Ch1 Value = %d\n", adcValue);
		printf("습도센서전압 : %f\n", humiVolt);
		printf("현재습도 : %f \n", humi);
		printf("\n\n------------------------\n\n");
		delay(2000);

	}

	return 0;
}

int read_mcp3208_adc(unsigned char adcChannel)
{
	unsigned char buff[3];
	int adcValue = 0;

	buff[0] = 0x06 | ((adcChannel & 0x07) >> 2);
	buff[1] = ((adcChannel & 0x07) << 6);
	buff[2] = 0x00;

	digitalWrite(BCM_GPIO, 0); // Low : CS Active

	wiringPiSPIDataRW(SPI_CHANNEL, buff, 3);

	buff[1] = 0x0F & buff[1];
	adcValue = (buff[1] << 8) | buff[2];

	digitalWrite(BCM_GPIO, 1); // High : CS Inactive

	return adcValue;
}
