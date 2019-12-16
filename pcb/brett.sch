EESchema Schematic File Version 4
LIBS:brett-cache
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 7
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L 74xx:74LS138 U1
U 1 1 5D588B57
P 6850 3200
F 0 "U1" H 6700 3850 50  0000 C CNN
F 1 "74LS138" H 6600 3700 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 6850 3200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS138" H 6850 3200 50  0001 C CNN
	1    6850 3200
	1    0    0    -1  
$EndComp
$Sheet
S 8200 1550 650  450 
U 5D5B6A4A
F0 "Stepper A" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 1650 50 
F3 "DIR" I L 8200 1800 50 
F4 "STEP" I L 8200 1900 50 
F5 "DCO_ES" O R 8850 1900 50 
$EndSheet
Wire Wire Line
	8200 1800 7800 1800
Text Label 7800 1800 0    50   ~ 0
A_DIR
Wire Wire Line
	7800 1900 8200 1900
Text Label 7800 1900 0    50   ~ 0
A_STP
$Comp
L power:+24V #PWR0101
U 1 1 5D595B20
P 4800 6550
F 0 "#PWR0101" H 4800 6400 50  0001 C CNN
F 1 "+24V" H 4815 6723 50  0000 C CNN
F 2 "" H 4800 6550 50  0001 C CNN
F 3 "" H 4800 6550 50  0001 C CNN
	1    4800 6550
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5D59826E
P 4800 7150
F 0 "#PWR0102" H 4800 6900 50  0001 C CNN
F 1 "GND" V 4805 7022 50  0000 R CNN
F 2 "" H 4800 7150 50  0001 C CNN
F 3 "" H 4800 7150 50  0001 C CNN
	1    4800 7150
	0    -1   -1   0   
$EndComp
$Comp
L Device:Polyfuse F1
U 1 1 5D599259
P 2050 6550
F 0 "F1" V 1800 6550 50  0000 C CNN
F 1 "Polyfuse" V 1900 6550 50  0000 C CNN
F 2 "Fuse:Fuse_Bourns_MF-RHT1000" H 2100 6350 50  0001 L CNN
F 3 "~" H 2050 6550 50  0001 C CNN
	1    2050 6550
	0    1    1    0   
$EndComp
$Comp
L Device:CP_Small C1
U 1 1 5D5973D1
P 2650 6850
AR Path="/5D5973D1" Ref="C1"  Part="1" 
AR Path="/5D5B6A4A/5D5973D1" Ref="C?"  Part="1" 
F 0 "C1" H 2738 6896 50  0000 L CNN
F 1 "100u" H 2738 6805 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 2650 6850 50  0001 C CNN
F 3 "~" H 2650 6850 50  0001 C CNN
	1    2650 6850
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C2
U 1 1 5D59BC91
P 3050 6850
F 0 "C2" H 3142 6896 50  0000 L CNN
F 1 "100n" H 3142 6805 50  0000 L CNN
F 2 "Capacitor_THT:C_Radial_D6.3mm_H5.0mm_P2.50mm" H 3050 6850 50  0001 C CNN
F 3 "~" H 3050 6850 50  0001 C CNN
	1    3050 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 7150 2650 7150
Connection ~ 2650 7150
Wire Wire Line
	2650 6550 2650 6750
Wire Wire Line
	2650 6550 3050 6550
Wire Wire Line
	3050 6550 3050 6750
Connection ~ 2650 6550
Wire Wire Line
	2650 6950 2650 7150
Wire Wire Line
	3050 6950 3050 7150
Connection ~ 3050 6550
Wire Wire Line
	1700 6550 1900 6550
$Comp
L Connector:Screw_Terminal_01x02 J1
U 1 1 5D59EF55
P 1500 6550
F 0 "J1" H 1418 6225 50  0000 C CNN
F 1 "Screw_Terminal_01x02" H 1750 6300 50  0000 C CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00232_1x02_P5.08mm_Horizontal" H 1500 6550 50  0001 C CNN
F 3 "~" H 1500 6550 50  0001 C CNN
	1    1500 6550
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3050 6550 3450 6550
Wire Wire Line
	1800 7150 1800 6650
Wire Wire Line
	1800 6650 1700 6650
Connection ~ 3450 6550
Wire Wire Line
	3450 6550 4800 6550
Wire Wire Line
	1800 7150 2650 7150
$Comp
L Jumper:SolderJumper_3_Open JP2
U 1 1 5D5DCECA
P 9150 9600
F 0 "JP2" V 9300 9250 50  0000 L CNN
F 1 "SolderJumper_3_Open" V 9195 9668 50  0001 L CNN
F 2 "Jumper:SolderJumper-3_P1.3mm_Open_RoundedPad1.0x1.5mm" H 9150 9600 50  0001 C CNN
F 3 "~" H 9150 9600 50  0001 C CNN
	1    9150 9600
	0    -1   -1   0   
$EndComp
Text Notes 8900 8800 0    200  ~ 0
Stepper Config
$Comp
L power:GND #PWR0103
U 1 1 5D5E7450
P 8950 9850
F 0 "#PWR0103" H 8950 9600 50  0001 C CNN
F 1 "GND" H 8955 9677 50  0000 C CNN
F 2 "" H 8950 9850 50  0001 C CNN
F 3 "" H 8950 9850 50  0001 C CNN
	1    8950 9850
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR0104
U 1 1 5D5E7B7C
P 8950 9300
F 0 "#PWR0104" H 8950 9150 50  0001 C CNN
F 1 "+3V3" H 8965 9473 50  0000 C CNN
F 2 "" H 8950 9300 50  0001 C CNN
F 3 "" H 8950 9300 50  0001 C CNN
	1    8950 9300
	1    0    0    -1  
$EndComp
Wire Wire Line
	8950 9300 8950 9350
Wire Wire Line
	8950 9350 9150 9350
Wire Wire Line
	8950 9850 9150 9850
Wire Wire Line
	9150 9850 9150 9800
Wire Wire Line
	9150 9350 9150 9400
Connection ~ 9150 9350
Text GLabel 9350 9600 2    50   Output ~ 0
MISO
Wire Wire Line
	9300 9600 9350 9600
Connection ~ 9150 9850
$Comp
L Jumper:SolderJumper_3_Open JP3
U 1 1 5D5EFA64
P 9750 9600
F 0 "JP3" V 9900 9250 50  0000 L CNN
F 1 "SolderJumper_3_Open" V 9795 9668 50  0001 L CNN
F 2 "Jumper:SolderJumper-3_P1.3mm_Open_RoundedPad1.0x1.5mm" H 9750 9600 50  0001 C CNN
F 3 "~" H 9750 9600 50  0001 C CNN
	1    9750 9600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9750 9850 9750 9800
Wire Wire Line
	9750 9350 9750 9400
Text GLabel 9950 9600 2    50   Output ~ 0
MOSI
Wire Wire Line
	9900 9600 9950 9600
$Comp
L Jumper:SolderJumper_3_Open JP4
U 1 1 5D5F0C87
P 10350 9600
F 0 "JP4" V 10500 9250 50  0000 L CNN
F 1 "SolderJumper_3_Open" V 10395 9668 50  0001 L CNN
F 2 "Jumper:SolderJumper-3_P1.3mm_Open_RoundedPad1.0x1.5mm" H 10350 9600 50  0001 C CNN
F 3 "~" H 10350 9600 50  0001 C CNN
	1    10350 9600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	10350 9850 10350 9800
Wire Wire Line
	10350 9350 10350 9400
Wire Wire Line
	10500 9600 10550 9600
Wire Wire Line
	9150 9850 9750 9850
Wire Wire Line
	9150 9350 9750 9350
Text GLabel 10550 9600 2    50   Output ~ 0
SCK
Text Notes 1600 6050 0    200  ~ 0
Power
$Comp
L Regulator_Switching:TSR_1-2450 U2
U 1 1 5D63A20A
P 3950 6850
F 0 "U2" H 4100 6650 50  0000 C CNN
F 1 "TSR_1-2450" H 3600 6650 50  0000 C CNN
F 2 "Converter_DCDC:Converter_DCDC_TRACO_TSR-1_THT" H 3950 6700 50  0001 L CIN
F 3 "http://www.tracopower.com/products/tsr1.pdf" H 3950 6850 50  0001 C CNN
	1    3950 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 6750 3550 6750
Wire Wire Line
	3450 6550 3450 6750
Wire Wire Line
	3050 7150 3950 7150
Wire Wire Line
	3950 7150 3950 7050
Connection ~ 3050 7150
$Comp
L power:+5V #PWR0105
U 1 1 5D6416C5
P 4800 6750
F 0 "#PWR0105" H 4800 6600 50  0001 C CNN
F 1 "+5V" V 4815 6878 50  0000 L CNN
F 2 "" H 4800 6750 50  0001 C CNN
F 3 "" H 4800 6750 50  0001 C CNN
	1    4800 6750
	0    1    1    0   
$EndComp
Wire Wire Line
	4350 6750 4500 6750
Wire Wire Line
	3950 7150 4500 7150
Connection ~ 3950 7150
$Comp
L Device:CP_Small C4
U 1 1 5D643DCC
P 4500 6950
AR Path="/5D643DCC" Ref="C4"  Part="1" 
AR Path="/5D5B6A4A/5D643DCC" Ref="C?"  Part="1" 
F 0 "C4" H 4588 6996 50  0000 L CNN
F 1 "100u" H 4588 6905 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 4500 6950 50  0001 C CNN
F 3 "~" H 4500 6950 50  0001 C CNN
	1    4500 6950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 6750 4500 6850
Connection ~ 4500 6750
Wire Wire Line
	4500 6750 4800 6750
Wire Wire Line
	4500 7050 4500 7150
Connection ~ 4500 7150
Wire Wire Line
	4500 7150 4800 7150
Wire Wire Line
	2200 6550 2650 6550
Text GLabel 2300 3150 0    50   Input ~ 0
MISO
Text GLabel 2300 3050 0    50   Input ~ 0
MOSI
Wire Wire Line
	2300 3050 2500 3050
Wire Wire Line
	2500 2950 2300 2950
$Comp
L power:+5V #PWR0111
U 1 1 5D64CC3C
P 3800 1850
F 0 "#PWR0111" H 3800 1700 50  0001 C CNN
F 1 "+5V" V 3815 1978 50  0000 L CNN
F 2 "" H 3800 1850 50  0001 C CNN
F 3 "" H 3800 1850 50  0001 C CNN
	1    3800 1850
	0    1    1    0   
$EndComp
Wire Wire Line
	3800 1850 3500 1850
$Comp
L power:GND #PWR0112
U 1 1 5D64FA36
P 3800 1750
F 0 "#PWR0112" H 3800 1500 50  0001 C CNN
F 1 "GND" V 3805 1622 50  0000 R CNN
F 2 "" H 3800 1750 50  0001 C CNN
F 3 "" H 3800 1750 50  0001 C CNN
	1    3800 1750
	0    -1   -1   0   
$EndComp
$Comp
L power:+5V #PWR0113
U 1 1 5D65289F
P 2200 1850
F 0 "#PWR0113" H 2200 1700 50  0001 C CNN
F 1 "+5V" V 2215 1978 50  0000 L CNN
F 2 "" H 2200 1850 50  0001 C CNN
F 3 "" H 2200 1850 50  0001 C CNN
	1    2200 1850
	0    -1   1    0   
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5D6528A6
P 2200 1750
F 0 "#PWR0114" H 2200 1500 50  0001 C CNN
F 1 "GND" V 2205 1622 50  0000 R CNN
F 2 "" H 2200 1750 50  0001 C CNN
F 3 "" H 2200 1750 50  0001 C CNN
	1    2200 1750
	0    1    -1   0   
$EndComp
$Comp
L power:+3V3 #PWR0115
U 1 1 5D655747
P 2200 2150
F 0 "#PWR0115" H 2200 2000 50  0001 C CNN
F 1 "+3V3" V 2215 2278 50  0000 L CNN
F 2 "" H 2200 2150 50  0001 C CNN
F 3 "" H 2200 2150 50  0001 C CNN
	1    2200 2150
	0    -1   -1   0   
$EndComp
$Comp
L power:+3V3 #PWR0116
U 1 1 5D65731C
P 3800 2150
F 0 "#PWR0116" H 3800 2000 50  0001 C CNN
F 1 "+3V3" V 3800 2300 50  0000 L CNN
F 2 "" H 3800 2150 50  0001 C CNN
F 3 "" H 3800 2150 50  0001 C CNN
	1    3800 2150
	0    1    1    0   
$EndComp
Wire Wire Line
	2200 1850 2500 1850
Wire Wire Line
	2500 1750 2300 1750
Wire Wire Line
	3800 1750 3700 1750
Wire Wire Line
	2500 2050 2300 2050
Wire Wire Line
	2300 2050 2300 1750
Connection ~ 2300 1750
Wire Wire Line
	2300 1750 2200 1750
Wire Wire Line
	3500 2050 3700 2050
Wire Wire Line
	3700 2050 3700 1750
Connection ~ 3700 1750
Wire Wire Line
	3700 1750 3500 1750
NoConn ~ 2500 1950
NoConn ~ 3500 1950
$Comp
L Transistor_BJT:BC547 Q1
U 1 1 5D670AE2
P 2450 9700
F 0 "Q1" H 2641 9746 50  0000 L CNN
F 1 "BC547" H 2641 9655 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 2650 9625 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/BC/BC547.pdf" H 2450 9700 50  0001 L CNN
	1    2450 9700
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR0117
U 1 1 5D672A3E
P 1850 9700
F 0 "#PWR0117" H 1850 9550 50  0001 C CNN
F 1 "+24V" V 1865 9828 50  0000 L CNN
F 2 "" H 1850 9700 50  0001 C CNN
F 3 "" H 1850 9700 50  0001 C CNN
	1    1850 9700
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_Small R1
U 1 1 5D675738
P 2050 9700
F 0 "R1" V 2246 9700 50  0000 C CNN
F 1 "100kOhm" V 2155 9700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 2050 9700 50  0001 C CNN
F 3 "~" H 2050 9700 50  0001 C CNN
	1    2050 9700
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2150 9700 2250 9700
Wire Wire Line
	1850 9700 1950 9700
Wire Wire Line
	2550 9400 2550 9500
$Comp
L power:+3V3 #PWR0118
U 1 1 5D68976C
P 2550 9000
F 0 "#PWR0118" H 2550 8850 50  0001 C CNN
F 1 "+3V3" H 2565 9173 50  0000 C CNN
F 2 "" H 2550 9000 50  0001 C CNN
F 3 "" H 2550 9000 50  0001 C CNN
	1    2550 9000
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R2
U 1 1 5D6AD63C
P 2550 9200
F 0 "R2" H 2609 9246 50  0000 L CNN
F 1 "10k" H 2609 9155 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 2550 9200 50  0001 C CNN
F 3 "~" H 2550 9200 50  0001 C CNN
	1    2550 9200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 9400 2550 9300
Connection ~ 2550 9400
Wire Wire Line
	2550 9100 2550 9000
$Comp
L power:GND #PWR0119
U 1 1 5D6732F5
P 2550 10100
F 0 "#PWR0119" H 2550 9850 50  0001 C CNN
F 1 "GND" H 2555 9927 50  0000 C CNN
F 2 "" H 2550 10100 50  0001 C CNN
F 3 "" H 2550 10100 50  0001 C CNN
	1    2550 10100
	1    0    0    -1  
$EndComp
Text GLabel 3100 9400 2    50   Input ~ 0
DISABLE_OUT
Wire Wire Line
	2550 10000 2550 10100
Wire Wire Line
	2550 9900 2550 10000
Connection ~ 2550 10000
Wire Wire Line
	3000 10000 2550 10000
Wire Wire Line
	3000 9800 3000 10000
Wire Wire Line
	3000 9400 2550 9400
Connection ~ 3000 9400
Wire Wire Line
	3000 9600 3000 9400
$Comp
L Device:C_Small _C1
U 1 1 5D680594
P 3000 9700
F 0 "_C1" H 3092 9746 50  0000 L CNN
F 1 "1n" H 3092 9655 50  0000 L CNN
F 2 "Capacitor_THT:C_Radial_D6.3mm_H5.0mm_P2.50mm" H 3000 9700 50  0001 C CNN
F 3 "~" H 3000 9700 50  0001 C CNN
	1    3000 9700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 9400 3100 9400
Wire Wire Line
	2500 3450 2200 3450
Text Label 3800 2650 2    50   ~ 0
F_DIR
Wire Wire Line
	2500 3350 2200 3350
Text Label 3800 2550 2    50   ~ 0
F_STP
Wire Wire Line
	2500 2750 2200 2750
Text Label 2200 2250 0    50   ~ 0
A_DIR
Wire Wire Line
	2500 2650 2200 2650
Text Label 2200 2350 0    50   ~ 0
A_STP
Wire Wire Line
	2500 2550 2200 2550
Text Label 2200 2450 0    50   ~ 0
B_DIR
Wire Wire Line
	2500 2450 2200 2450
Text Label 2200 2550 0    50   ~ 0
B_STP
Wire Wire Line
	2500 2350 2200 2350
Text Label 2200 3350 0    50   ~ 0
C_DIR
Wire Wire Line
	2500 2250 2200 2250
Text Label 2200 3450 0    50   ~ 0
C_STP
Wire Wire Line
	3500 2350 3800 2350
Text Label 4100 3250 2    50   ~ 0
D_DIR
Wire Wire Line
	3500 2450 3800 2450
Text Label 4100 3150 2    50   ~ 0
D_STP
Wire Wire Line
	3500 2550 3800 2550
Text Label 4100 2850 2    50   ~ 0
E_DIR
Wire Wire Line
	3500 2650 3800 2650
Text Label 4300 2750 2    50   ~ 0
E_STP
Wire Wire Line
	3500 3650 3800 3650
Text Label 3800 3450 2    50   ~ 0
A_FB
Wire Wire Line
	3500 3550 3800 3550
Text Label 3800 3550 2    50   ~ 0
B_FB
Wire Wire Line
	3500 3450 3800 3450
Text Label 3800 3650 2    50   ~ 0
C_FB
Wire Wire Line
	3500 3350 3800 3350
Text Label 3800 3350 2    50   ~ 0
D_FB
Wire Wire Line
	3500 3050 3800 3050
Text Label 3800 3050 2    50   ~ 0
E_FB
Wire Wire Line
	3500 2950 3800 2950
Text Label 3800 2950 2    50   ~ 0
F_FB
Wire Wire Line
	2500 3550 2000 3550
Text Label 2000 3550 0    50   ~ 0
SDA
Wire Wire Line
	2500 3250 2000 3250
Text Label 2000 3250 0    50   ~ 0
SCL
Wire Wire Line
	3500 3250 4100 3250
Text Label 2200 2650 0    50   ~ 0
CS_0
Text Label 2200 2750 0    50   ~ 0
CS_1
Wire Wire Line
	3500 2850 4100 2850
Text Label 2200 2850 0    50   ~ 0
CS_2
Wire Wire Line
	6350 2900 6050 2900
Wire Wire Line
	6350 3000 6050 3000
Text Label 6050 3000 0    50   ~ 0
CS_1
Wire Wire Line
	6350 3100 6050 3100
$Comp
L power:+3V3 #PWR0120
U 1 1 5D7A47C4
P 6850 2500
F 0 "#PWR0120" H 6850 2350 50  0001 C CNN
F 1 "+3V3" H 6865 2673 50  0000 C CNN
F 2 "" H 6850 2500 50  0001 C CNN
F 3 "" H 6850 2500 50  0001 C CNN
	1    6850 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 2500 6850 2600
$Comp
L power:GND #PWR0121
U 1 1 5D7A8813
P 6850 4000
F 0 "#PWR0121" H 6850 3750 50  0001 C CNN
F 1 "GND" H 6855 3827 50  0000 C CNN
F 2 "" H 6850 4000 50  0001 C CNN
F 3 "" H 6850 4000 50  0001 C CNN
	1    6850 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6850 3900 6850 4000
$Comp
L Connector:Conn_01x04_Female JI2C1
U 1 1 5D7B3556
P 6950 9700
F 0 "JI2C1" H 6978 9676 50  0000 L CNN
F 1 "Conn_01x04_Female" H 6978 9585 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 6950 9700 50  0001 C CNN
F 3 "~" H 6950 9700 50  0001 C CNN
	1    6950 9700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0122
U 1 1 5D7B40FC
P 5850 9700
F 0 "#PWR0122" H 5850 9450 50  0001 C CNN
F 1 "GND" V 5855 9572 50  0000 R CNN
F 2 "" H 5850 9700 50  0001 C CNN
F 3 "" H 5850 9700 50  0001 C CNN
	1    5850 9700
	0    1    1    0   
$EndComp
$Comp
L power:+3V3 #PWR0123
U 1 1 5D7B4A7A
P 5850 9300
F 0 "#PWR0123" H 5850 9150 50  0001 C CNN
F 1 "+3V3" V 5865 9428 50  0000 L CNN
F 2 "" H 5850 9300 50  0001 C CNN
F 3 "" H 5850 9300 50  0001 C CNN
	1    5850 9300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5850 9300 6200 9300
Wire Wire Line
	6700 9300 6700 9600
Wire Wire Line
	6700 9600 6750 9600
$Comp
L Device:R_Small R3
U 1 1 5D7C72A2
P 6200 9500
F 0 "R3" H 6259 9546 50  0000 L CNN
F 1 "4k7" H 6259 9455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 6200 9500 50  0001 C CNN
F 3 "~" H 6200 9500 50  0001 C CNN
	1    6200 9500
	1    0    0    -1  
$EndComp
$Comp
L Device:R_Small R4
U 1 1 5D7C84A5
P 6450 9500
F 0 "R4" H 6509 9546 50  0000 L CNN
F 1 "4k7" H 6509 9455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 6450 9500 50  0001 C CNN
F 3 "~" H 6450 9500 50  0001 C CNN
	1    6450 9500
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 9700 6750 9700
Wire Wire Line
	6200 9300 6200 9400
Connection ~ 6200 9300
Wire Wire Line
	6200 9300 6450 9300
Wire Wire Line
	6450 9300 6450 9400
Connection ~ 6450 9300
Wire Wire Line
	6450 9300 6700 9300
Wire Wire Line
	6450 9600 6450 9800
Wire Wire Line
	6450 9800 6750 9800
Wire Wire Line
	6200 9600 6200 9900
Wire Wire Line
	6200 9900 6750 9900
Wire Wire Line
	6450 9800 5850 9800
Connection ~ 6450 9800
Wire Wire Line
	6200 9900 5850 9900
Connection ~ 6200 9900
Text Label 5850 9800 0    50   ~ 0
SDA
Text Label 5850 9900 0    50   ~ 0
SCL
Text Notes 5500 8850 0    200  ~ 0
I2C
Connection ~ 9750 9350
Wire Wire Line
	9750 9350 10350 9350
Connection ~ 9750 9850
Wire Wire Line
	9750 9850 10350 9850
Text Notes 1600 8600 0    200  ~ 0
Protection
Text Notes 5950 6000 0    200  ~ 0
Fan
$Comp
L Transistor_BJT:BC547 Q2
U 1 1 5D8A2EE0
P 7250 6900
F 0 "Q2" H 7441 6946 50  0000 L CNN
F 1 "BC547" H 7441 6855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 7450 6825 50  0001 L CIN
F 3 "http://www.fairchildsemi.com/ds/BC/BC547.pdf" H 7250 6900 50  0001 L CNN
	1    7250 6900
	1    0    0    -1  
$EndComp
$Comp
L power:+24V #PWR0124
U 1 1 5D8A3BE8
P 7050 6300
F 0 "#PWR0124" H 7050 6150 50  0001 C CNN
F 1 "+24V" H 7065 6473 50  0000 C CNN
F 2 "" H 7050 6300 50  0001 C CNN
F 3 "" H 7050 6300 50  0001 C CNN
	1    7050 6300
	1    0    0    -1  
$EndComp
Wire Wire Line
	7050 6300 7050 6500
Wire Wire Line
	7050 6500 7450 6500
$Comp
L Connector:Conn_01x02_Male J3
U 1 1 5D8AB074
P 7650 6600
F 0 "J3" H 7622 6482 50  0000 R CNN
F 1 "Conn_01x02_Male" H 7622 6573 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 7650 6600 50  0001 C CNN
F 3 "~" H 7650 6600 50  0001 C CNN
	1    7650 6600
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0125
U 1 1 5D8B97D2
P 7350 7250
F 0 "#PWR0125" H 7350 7000 50  0001 C CNN
F 1 "GND" H 7355 7077 50  0000 C CNN
F 2 "" H 7350 7250 50  0001 C CNN
F 3 "" H 7350 7250 50  0001 C CNN
	1    7350 7250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7350 7100 7350 7250
Wire Wire Line
	7450 6600 7350 6600
Wire Wire Line
	7350 6600 7350 6700
$Comp
L Device:R_Small R5
U 1 1 5D8C32D5
P 6850 6900
F 0 "R5" V 6654 6900 50  0000 C CNN
F 1 "1k" V 6745 6900 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" H 6850 6900 50  0001 C CNN
F 3 "~" H 6850 6900 50  0001 C CNN
	1    6850 6900
	0    1    1    0   
$EndComp
Wire Wire Line
	7050 6900 6950 6900
Text Label 6100 6600 0    50   ~ 0
AUX0
Text Notes 6900 7050 2    50   ~ 0
3mA
Text Notes 7950 6700 2    50   ~ 0
max. 300mA
$Comp
L Jumper:SolderJumper_3_Bridged12 JP?
U 1 1 5D8DE6FB
P 6500 6900
AR Path="/5D5B6A4A/5D8DE6FB" Ref="JP?"  Part="1" 
AR Path="/5D8DE6FB" Ref="JP1"  Part="1" 
F 0 "JP1" V 6400 6700 50  0000 L CNN
F 1 "SolderJumper_3_Bridged12" H 6500 7014 50  0001 C CNN
F 2 "Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm" H 6500 6900 50  0001 C CNN
F 3 "~" H 6500 6900 50  0001 C CNN
	1    6500 6900
	0    -1   1    0   
$EndComp
Wire Wire Line
	6650 6900 6750 6900
$Comp
L power:+3V3 #PWR0126
U 1 1 5D917ECD
P 6400 7200
F 0 "#PWR0126" H 6400 7050 50  0001 C CNN
F 1 "+3V3" V 6415 7328 50  0000 L CNN
F 2 "" H 6400 7200 50  0001 C CNN
F 3 "" H 6400 7200 50  0001 C CNN
	1    6400 7200
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6400 7200 6500 7200
Wire Wire Line
	6500 7200 6500 7100
Wire Wire Line
	6500 6600 6500 6700
Wire Wire Line
	6100 6600 6500 6600
Text Label 3800 2350 2    50   ~ 0
AUX0
Wire Wire Line
	3500 2750 4300 2750
Text Label 3800 2450 2    50   ~ 0
AUX1
Text Notes 9500 6000 0    200  ~ 0
Auxiliaries
Wire Wire Line
	10100 6450 9500 6450
Text Label 9500 6450 0    50   ~ 0
AUX1
Wire Wire Line
	10100 6550 9500 6550
Text Label 9500 6550 0    50   ~ 0
AUX0
$Comp
L power:GND #PWR0127
U 1 1 5D95F857
P 9750 6750
F 0 "#PWR0127" H 9750 6500 50  0001 C CNN
F 1 "GND" V 9755 6622 50  0000 R CNN
F 2 "" H 9750 6750 50  0001 C CNN
F 3 "" H 9750 6750 50  0001 C CNN
	1    9750 6750
	0    1    -1   0   
$EndComp
$Comp
L power:+3V3 #PWR0128
U 1 1 5D960208
P 9750 6650
F 0 "#PWR0128" H 9750 6500 50  0001 C CNN
F 1 "+3V3" V 9765 6778 50  0000 L CNN
F 2 "" H 9750 6650 50  0001 C CNN
F 3 "" H 9750 6650 50  0001 C CNN
	1    9750 6650
	0    -1   -1   0   
$EndComp
Wire Wire Line
	9750 6650 10100 6650
Wire Wire Line
	10100 6750 9750 6750
Text Label 9150 1900 2    50   ~ 0
A_FB
Wire Wire Line
	8850 1900 9150 1900
Text Notes 2200 9900 2    50   ~ 0
0.2mA
Text Label 6050 3100 0    50   ~ 0
CS_2
Text Label 6050 2900 0    50   ~ 0
CS_0
$Sheet
S 8200 2200 650  450 
U 5D623EE0
F0 "Stepper B" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 2300 50 
F3 "DIR" I L 8200 2450 50 
F4 "STEP" I L 8200 2550 50 
F5 "DCO_ES" O R 8850 2550 50 
$EndSheet
Wire Wire Line
	8200 2450 7800 2450
Text Label 7800 2450 0    50   ~ 0
B_DIR
Wire Wire Line
	7800 2550 8200 2550
Text Label 7800 2550 0    50   ~ 0
B_STP
Text Label 9150 2550 2    50   ~ 0
B_FB
Wire Wire Line
	8850 2550 9150 2550
$Sheet
S 8200 2850 650  450 
U 5D636373
F0 "Stepper C" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 2950 50 
F3 "DIR" I L 8200 3100 50 
F4 "STEP" I L 8200 3200 50 
F5 "DCO_ES" O R 8850 3200 50 
$EndSheet
Wire Wire Line
	8200 3100 7800 3100
Text Label 7800 3100 0    50   ~ 0
C_DIR
Wire Wire Line
	7800 3200 8200 3200
Text Label 7800 3200 0    50   ~ 0
C_STP
Text Label 9150 3200 2    50   ~ 0
C_FB
Wire Wire Line
	8850 3200 9150 3200
$Sheet
S 8200 3500 650  450 
U 5D63CA73
F0 "Stepper D" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 3600 50 
F3 "DIR" I L 8200 3750 50 
F4 "STEP" I L 8200 3850 50 
F5 "DCO_ES" O R 8850 3850 50 
$EndSheet
Wire Wire Line
	8200 3750 7800 3750
Text Label 7800 3750 0    50   ~ 0
D_DIR
Wire Wire Line
	7800 3850 8200 3850
Text Label 7800 3850 0    50   ~ 0
D_STP
Text Label 9150 3850 2    50   ~ 0
D_FB
Wire Wire Line
	8850 3850 9150 3850
$Sheet
S 8200 4150 650  450 
U 5D64352A
F0 "Stepper E" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 4250 50 
F3 "DIR" I L 8200 4400 50 
F4 "STEP" I L 8200 4500 50 
F5 "DCO_ES" O R 8850 4500 50 
$EndSheet
Wire Wire Line
	8200 4400 7800 4400
Text Label 7800 4400 0    50   ~ 0
E_DIR
Wire Wire Line
	7800 4500 8200 4500
Text Label 7800 4500 0    50   ~ 0
E_STP
Text Label 9150 4500 2    50   ~ 0
E_FB
Wire Wire Line
	8850 4500 9150 4500
$Sheet
S 8200 4800 650  450 
U 5D64A60D
F0 "Stepper F" 50
F1 "stepper_output.sch" 50
F2 "CS" I L 8200 4900 50 
F3 "DIR" I L 8200 5050 50 
F4 "STEP" I L 8200 5150 50 
F5 "DCO_ES" O R 8850 5150 50 
$EndSheet
Wire Wire Line
	8200 5050 7800 5050
Text Label 7800 5050 0    50   ~ 0
F_DIR
Wire Wire Line
	7800 5150 8200 5150
Text Label 7800 5150 0    50   ~ 0
F_STP
Text Label 9150 5150 2    50   ~ 0
F_FB
Wire Wire Line
	8850 5150 9150 5150
Wire Wire Line
	8200 2950 7650 2950
Wire Wire Line
	7600 3600 7600 3000
Wire Wire Line
	7600 3600 8200 3600
Wire Wire Line
	7500 4250 8200 4250
Wire Wire Line
	8200 4900 7400 4900
Wire Wire Line
	7550 2300 8200 2300
Wire Wire Line
	8200 1650 7450 1650
Wire Wire Line
	7400 4900 7400 3200
NoConn ~ 7350 2900
Text Notes 7600 1050 0    200  ~ 0
Steppers
$Comp
L power:+3V3 #PWR0154
U 1 1 5D60C9AD
P 6150 3400
F 0 "#PWR0154" H 6150 3250 50  0001 C CNN
F 1 "+3V3" H 6165 3573 50  0000 C CNN
F 2 "" H 6150 3400 50  0001 C CNN
F 3 "" H 6150 3400 50  0001 C CNN
	1    6150 3400
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0155
U 1 1 5D628237
P 6150 3600
F 0 "#PWR0155" H 6150 3350 50  0001 C CNN
F 1 "GND" H 6155 3427 50  0000 C CNN
F 2 "" H 6150 3600 50  0001 C CNN
F 3 "" H 6150 3600 50  0001 C CNN
	1    6150 3600
	0    1    1    0   
$EndComp
Wire Wire Line
	6150 3600 6250 3600
Text GLabel 2300 2950 0    50   Input ~ 0
SCK
$Comp
L Connector:Conn_01x01_Male JRST1
U 1 1 5D633672
P 3800 2250
F 0 "JRST1" H 3650 2250 50  0000 C CNN
F 1 "Conn_01x01_Male" H 3908 2340 50  0001 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical" H 3800 2250 50  0001 C CNN
F 3 "~" H 3800 2250 50  0001 C CNN
	1    3800 2250
	-1   0    0    1   
$EndComp
Wire Wire Line
	3600 2250 3500 2250
$Comp
L power:GND #PWR0156
U 1 1 5D62C498
P 2450 3650
F 0 "#PWR0156" H 2450 3400 50  0001 C CNN
F 1 "GND" V 2455 3522 50  0000 R CNN
F 2 "" H 2450 3650 50  0001 C CNN
F 3 "" H 2450 3650 50  0001 C CNN
	1    2450 3650
	0    1    1    0   
$EndComp
Wire Wire Line
	3800 2150 3500 2150
Wire Wire Line
	2500 3150 2300 3150
Wire Wire Line
	2500 2150 2200 2150
Wire Wire Line
	3500 3150 4100 3150
$Comp
L SparkFun-Boards:ESP32_THING_W_ANT_KEEPOUT B0
U 1 1 5D4C381A
P 3000 2650
F 0 "B0" H 3000 4010 45  0000 C CNN
F 1 "ESP32_THING_W_ANT_KEEPOUT" H 3000 3926 45  0000 C CNN
F 2 "Boards:ESP32_THING" H 3000 3850 20  0001 C CNN
F 3 "" H 3000 2650 50  0001 C CNN
F 4 "DEV-13907" H 3000 3831 60  0000 C CNN "Feld4"
	1    3000 2650
	-1   0    0    1   
$EndComp
Wire Wire Line
	2500 3650 2450 3650
Wire Wire Line
	2500 2850 2200 2850
$Comp
L Connector:Conn_01x04_Male J2
U 1 1 5D67DF81
P 10300 6650
F 0 "J2" H 10272 6532 50  0000 R CNN
F 1 "Conn_01x04_Male" H 10272 6623 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 10300 6650 50  0001 C CNN
F 3 "~" H 10300 6650 50  0001 C CNN
	1    10300 6650
	-1   0    0    1   
$EndComp
Wire Wire Line
	7500 3100 7500 4250
Wire Wire Line
	7550 3500 7350 3500
Wire Wire Line
	7550 2300 7550 3500
Wire Wire Line
	7450 3400 7350 3400
Wire Wire Line
	7450 1650 7450 3400
Wire Wire Line
	7650 3300 7350 3300
Wire Wire Line
	7650 2950 7650 3300
$Comp
L power:GND #PWR0157
U 1 1 5D65EA9A
P 12850 6800
F 0 "#PWR0157" H 12850 6550 50  0001 C CNN
F 1 "GND" V 12855 6672 50  0000 R CNN
F 2 "" H 12850 6800 50  0001 C CNN
F 3 "" H 12850 6800 50  0001 C CNN
	1    12850 6800
	0    1    1    0   
$EndComp
$Comp
L power:+3V3 #PWR0158
U 1 1 5D65EAA0
P 12850 6700
F 0 "#PWR0158" H 12850 6550 50  0001 C CNN
F 1 "+3V3" V 12865 6828 50  0000 L CNN
F 2 "" H 12850 6700 50  0001 C CNN
F 3 "" H 12850 6700 50  0001 C CNN
	1    12850 6700
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x06_Male J4
U 1 1 5D671CF9
P 13450 6900
F 0 "J4" H 13422 6874 50  0000 R CNN
F 1 "Conn_01x06_Male" H 13422 6783 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 13450 6900 50  0001 C CNN
F 3 "~" H 13450 6900 50  0001 C CNN
	1    13450 6900
	-1   0    0    -1  
$EndComp
Text GLabel 12850 7100 0    50   Input ~ 0
MISO
Text GLabel 12850 7000 0    50   Input ~ 0
MOSI
Text GLabel 12850 6900 0    50   Input ~ 0
SCK
Wire Wire Line
	12850 6800 13250 6800
Wire Wire Line
	12850 7100 13250 7100
Wire Wire Line
	13250 7200 12850 7200
Text Label 12850 7200 0    50   ~ 0
CS_AUX
Text Label 7900 4050 2    50   ~ 0
CS_AUX
Wire Wire Line
	12850 6900 13250 6900
Wire Wire Line
	12850 7000 13250 7000
Wire Wire Line
	12850 6700 13250 6700
Wire Wire Line
	7400 3200 7350 3200
Wire Wire Line
	7500 3100 7350 3100
Wire Wire Line
	7350 3000 7600 3000
Wire Wire Line
	7350 3600 7350 4050
Wire Wire Line
	7350 4050 7900 4050
Text Notes 12450 6000 0    200  ~ 0
SPI
Text Notes 11900 3100 0    118  Italic 0
Revidieren:\n- Pull-Ups für FB-Pins\n- Vorwiderstände für JES-VCC\n- Diode bei 24V-Eingang\n- TMC2130 sind daisy-chainbar!\n- Bohrungen 3mm
Wire Wire Line
	6350 3500 6250 3500
Wire Wire Line
	6250 3500 6250 3600
Connection ~ 6250 3600
Wire Wire Line
	6250 3600 6350 3600
Wire Wire Line
	6150 3400 6350 3400
$EndSCHEMATC
