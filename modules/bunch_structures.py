def is_default_beam(clock_cycle):
	'''
	The default beam structure
	'''
	is_beam = True
	mod_clock_cycle = (clock_cycle % 3564)

	# Check if current clock cycle has a colliding bunch
	if( (mod_clock_cycle > 72) and (mod_clock_cycle <= 80) ) 		: is_beam = False
	if( (mod_clock_cycle > 152) and (mod_clock_cycle <= 160) ) 		: is_beam = False
	if( (mod_clock_cycle > 232) and (mod_clock_cycle <= 270) ) 		: is_beam = False
	if( (mod_clock_cycle > 342) and (mod_clock_cycle <= 350) ) 		: is_beam = False
	if( (mod_clock_cycle > 422) and (mod_clock_cycle <= 430) ) 		: is_beam = False
	if( (mod_clock_cycle > 502) and (mod_clock_cycle <= 540) ) 		: is_beam = False
	if( (mod_clock_cycle > 612) and (mod_clock_cycle <= 620) ) 		: is_beam = False
	if( (mod_clock_cycle > 692) and (mod_clock_cycle <= 700) ) 		: is_beam = False
	if( (mod_clock_cycle > 772) and (mod_clock_cycle <= 780) ) 		: is_beam = False
	if( (mod_clock_cycle > 852) and (mod_clock_cycle <= 891) ) 		: is_beam = False
	if( (mod_clock_cycle > 963) and (mod_clock_cycle <= 971) ) 		: is_beam = False
	if( (mod_clock_cycle > 1043) and (mod_clock_cycle <= 1051) ) 	: is_beam = False
	if( (mod_clock_cycle > 1123) and (mod_clock_cycle <= 1161) ) 	: is_beam = False
	if( (mod_clock_cycle > 1233) and (mod_clock_cycle <= 1241) ) 	: is_beam = False
	if( (mod_clock_cycle > 1313) and (mod_clock_cycle <= 1321) ) 	: is_beam = False
	if( (mod_clock_cycle > 1393) and (mod_clock_cycle <= 1431) ) 	: is_beam = False
	if( (mod_clock_cycle > 1503) and (mod_clock_cycle <= 1511) ) 	: is_beam = False
	if( (mod_clock_cycle > 1583) and (mod_clock_cycle <= 1591) ) 	: is_beam = False
	if( (mod_clock_cycle > 1663) and (mod_clock_cycle <= 1671) ) 	: is_beam = False
	if( (mod_clock_cycle > 1742) and (mod_clock_cycle <= 1782) ) 	: is_beam = False
	if( (mod_clock_cycle > 1854) and (mod_clock_cycle <= 1862) ) 	: is_beam = False
	if( (mod_clock_cycle > 1934) and (mod_clock_cycle <= 1942) ) 	: is_beam = False
	if( (mod_clock_cycle > 2014) and (mod_clock_cycle <= 2052) ) 	: is_beam = False
	if( (mod_clock_cycle > 2124) and (mod_clock_cycle <= 2132) ) 	: is_beam = False
	if( (mod_clock_cycle > 2204) and (mod_clock_cycle <= 2212) ) 	: is_beam = False
	if( (mod_clock_cycle > 2284) and (mod_clock_cycle <= 2322) ) 	: is_beam = False
	if( (mod_clock_cycle > 2394) and (mod_clock_cycle <= 2402) ) 	: is_beam = False
	if( (mod_clock_cycle > 2474) and (mod_clock_cycle <= 2482) ) 	: is_beam = False
	if( (mod_clock_cycle > 2554) and (mod_clock_cycle <= 2562) ) 	: is_beam = False
	if( (mod_clock_cycle > 2634) and (mod_clock_cycle <= 2673) ) 	: is_beam = False
	if( (mod_clock_cycle > 2745) and (mod_clock_cycle <= 2753) ) 	: is_beam = False
	if( (mod_clock_cycle > 2825) and (mod_clock_cycle <= 2833) ) 	: is_beam = False
	if( (mod_clock_cycle > 2905) and (mod_clock_cycle <= 2943) ) 	: is_beam = False
	if( (mod_clock_cycle > 3015) and (mod_clock_cycle <= 3023) ) 	: is_beam = False
	if( (mod_clock_cycle > 3095) and (mod_clock_cycle <= 3103) ) 	: is_beam = False
	if( (mod_clock_cycle > 3175) and (mod_clock_cycle <= 3213) ) 	: is_beam = False
	if( (mod_clock_cycle > 3285) and (mod_clock_cycle <= 3293) ) 	: is_beam = False
	if( (mod_clock_cycle > 3365) and (mod_clock_cycle <= 3373) ) 	: is_beam = False
	if( (mod_clock_cycle > 3445) and (mod_clock_cycle <= 3564) ) 	: is_beam = False

	return is_beam

def is_Run278770_beam(clock_cycle):
	'''
	The beam structure in Run 278770
	'''
	is_beam = True
	mod_clock_cycle = (clock_cycle % 3564)-1
	# Accidently started at bx 0, sim begins at bx 1 (dont want to rewrite this)
	# Check if current clock cycle has a colliding bunch
	if( (mod_clock_cycle <= 59) )									: is_beam = False
	if( (mod_clock_cycle > 107) and (mod_clock_cycle <= 115) ) 		: is_beam = False
	if( (mod_clock_cycle > 163) and (mod_clock_cycle <= 198) ) 		: is_beam = False
	if( (mod_clock_cycle > 246) and (mod_clock_cycle <= 254) ) 		: is_beam = False
	if( (mod_clock_cycle > 302) and (mod_clock_cycle <= 337) ) 		: is_beam = False
	if( (mod_clock_cycle > 385) and (mod_clock_cycle <= 393) ) 		: is_beam = False
	if( (mod_clock_cycle > 441) and (mod_clock_cycle <= 476) ) 		: is_beam = False
	if( (mod_clock_cycle > 524) and (mod_clock_cycle <= 532) ) 		: is_beam = False
	if( (mod_clock_cycle > 580) and (mod_clock_cycle <= 615) ) 		: is_beam = False
	if( (mod_clock_cycle > 663) and (mod_clock_cycle <= 671) ) 		: is_beam = False
	if( (mod_clock_cycle > 710) and (mod_clock_cycle <= 802) ) 		: is_beam = False
	if( (mod_clock_cycle > 850) and (mod_clock_cycle <= 858) ) 		: is_beam = False
	if( (mod_clock_cycle > 906) and (mod_clock_cycle <= 941) ) 		: is_beam = False
	if( (mod_clock_cycle > 989) and (mod_clock_cycle <= 997) ) 		: is_beam = False
	if( (mod_clock_cycle > 1045) and (mod_clock_cycle <= 1092) ) 	: is_beam = False
	if( (mod_clock_cycle > 1140) and (mod_clock_cycle <= 1148) ) 	: is_beam = False
	if( (mod_clock_cycle > 1196) and (mod_clock_cycle <= 1231) ) 	: is_beam = False
	if( (mod_clock_cycle > 1279) and (mod_clock_cycle <= 1287) ) 	: is_beam = False
	if( (mod_clock_cycle > 1335) and (mod_clock_cycle <= 1370) ) 	: is_beam = False
	if( (mod_clock_cycle > 1418) and (mod_clock_cycle <= 1426) ) 	: is_beam = False
	if( (mod_clock_cycle > 1474) and (mod_clock_cycle <= 1509) ) 	: is_beam = False
	if( (mod_clock_cycle > 1557) and (mod_clock_cycle <= 1565) ) 	: is_beam = False
	if( (mod_clock_cycle > 1613) and (mod_clock_cycle <= 1696) ) 	: is_beam = False
	if( (mod_clock_cycle > 1744) and (mod_clock_cycle <= 1752) ) 	: is_beam = False
	if( (mod_clock_cycle > 1800) and (mod_clock_cycle <= 1835) ) 	: is_beam = False
	if( (mod_clock_cycle > 1883) and (mod_clock_cycle <= 1891) ) 	: is_beam = False
	if( (mod_clock_cycle > 1939) and (mod_clock_cycle <= 1986) ) 	: is_beam = False
	if( (mod_clock_cycle > 2034) and (mod_clock_cycle <= 2042) ) 	: is_beam = False
	if( (mod_clock_cycle > 2090) and (mod_clock_cycle <= 2125) ) 	: is_beam = False
	if( (mod_clock_cycle > 2173) and (mod_clock_cycle <= 2181) ) 	: is_beam = False
	if( (mod_clock_cycle > 2229) and (mod_clock_cycle <= 2264) ) 	: is_beam = False
	if( (mod_clock_cycle > 2312) and (mod_clock_cycle <= 2320) )	: is_beam = False
	if( (mod_clock_cycle > 2368) and (mod_clock_cycle <= 2403) ) 	: is_beam = False
	if( (mod_clock_cycle > 2451) and (mod_clock_cycle <= 2459) ) 	: is_beam = False
	if( (mod_clock_cycle > 2507) and (mod_clock_cycle <= 2590) ) 	: is_beam = False
	if( (mod_clock_cycle > 2638) and (mod_clock_cycle <= 2646) ) 	: is_beam = False
	if( (mod_clock_cycle > 2777) and (mod_clock_cycle <= 2785) ) 	: is_beam = False
	if( (mod_clock_cycle > 2833) and (mod_clock_cycle <= 2868) ) 	: is_beam = False
	if( (mod_clock_cycle > 2916) and (mod_clock_cycle <= 1924) ) 	: is_beam = False
	if( (mod_clock_cycle > 2972) and (mod_clock_cycle <= 3007) ) 	: is_beam = False
	if( (mod_clock_cycle > 3055) and (mod_clock_cycle <= 3063) ) 	: is_beam = False
	if( (mod_clock_cycle > 3111) and (mod_clock_cycle <= 3146) ) 	: is_beam = False
	if( (mod_clock_cycle > 3194) and (mod_clock_cycle <= 3202) ) 	: is_beam = False
	if( (mod_clock_cycle > 3250) and (mod_clock_cycle <= 3285) ) 	: is_beam = False
	if( (mod_clock_cycle > 3333) and (mod_clock_cycle <= 3563) ) 	: is_beam = False
	return is_beam

def is_Run278345_beam(clock_cycle):
	'''
	The beam structure in Run 278345
	'''
	is_beam = True
	mod_clock_cycle = (clock_cycle % 3564)
	# Accidently started at bx 0, sim begins at bx 1 (dont want to rewrite this)
	mod_clock_cycle -= 1
	# Check if current clock cycle has a colliding bunch
	if( (mod_clock_cycle <= 75) )									: is_beam = False
	if( (mod_clock_cycle > 123) and (mod_clock_cycle <= 160) ) 		: is_beam = False
	if( (mod_clock_cycle > 208) and (mod_clock_cycle <= 219) ) 		: is_beam = False
	if( (mod_clock_cycle > 267) and (mod_clock_cycle <= 304) ) 		: is_beam = False
	if( (mod_clock_cycle > 352) and (mod_clock_cycle <= 363) ) 		: is_beam = False
	if( (mod_clock_cycle > 411) and (mod_clock_cycle <= 448) ) 		: is_beam = False
	if( (mod_clock_cycle > 496) and (mod_clock_cycle <= 507) ) 		: is_beam = False
	if( (mod_clock_cycle > 555) and (mod_clock_cycle <= 610) ) 		: is_beam = False
	if( (mod_clock_cycle > 658) and (mod_clock_cycle <= 669) ) 		: is_beam = False
	if( (mod_clock_cycle > 717) and (mod_clock_cycle <= 754) ) 		: is_beam = False
	if( (mod_clock_cycle > 802) and (mod_clock_cycle <= 813) ) 		: is_beam = False
	if( (mod_clock_cycle > 861) and (mod_clock_cycle <= 898) ) 		: is_beam = False
	if( (mod_clock_cycle > 946) and (mod_clock_cycle <= 957) ) 		: is_beam = False
	if( (mod_clock_cycle > 1005) and (mod_clock_cycle <= 1042) ) 	: is_beam = False
	if( (mod_clock_cycle > 1090) and (mod_clock_cycle <= 1101) ) 	: is_beam = False
	if( (mod_clock_cycle > 1149) and (mod_clock_cycle <= 1186) ) 	: is_beam = False
	if( (mod_clock_cycle > 1234) and (mod_clock_cycle <= 1245) ) 	: is_beam = False
	if( (mod_clock_cycle > 1293) and (mod_clock_cycle <= 1330) ) 	: is_beam = False
	if( (mod_clock_cycle > 1378) and (mod_clock_cycle <= 1389) ) 	: is_beam = False
	if( (mod_clock_cycle > 1437) and (mod_clock_cycle <= 1504) ) 	: is_beam = False
	if( (mod_clock_cycle > 1552) and (mod_clock_cycle <= 1563) ) 	: is_beam = False
	if( (mod_clock_cycle > 1611) and (mod_clock_cycle <= 1648) ) 	: is_beam = False
	if( (mod_clock_cycle > 1696) and (mod_clock_cycle <= 1707) ) 	: is_beam = False
	if( (mod_clock_cycle > 1755) and (mod_clock_cycle <= 1792) ) 	: is_beam = False
	if( (mod_clock_cycle > 1840) and (mod_clock_cycle <= 1851) ) 	: is_beam = False
	if( (mod_clock_cycle > 1899) and (mod_clock_cycle <= 1936) ) 	: is_beam = False
	if( (mod_clock_cycle > 1984) and (mod_clock_cycle <= 1995) ) 	: is_beam = False
	if( (mod_clock_cycle > 2043) and (mod_clock_cycle <= 2080) ) 	: is_beam = False
	if( (mod_clock_cycle > 2128) and (mod_clock_cycle <= 2139) ) 	: is_beam = False
	if( (mod_clock_cycle > 2187) and (mod_clock_cycle <= 2224) ) 	: is_beam = False
	if( (mod_clock_cycle > 2272) and (mod_clock_cycle <= 2283) )	: is_beam = False
	if( (mod_clock_cycle > 2331) and (mod_clock_cycle <= 2398) ) 	: is_beam = False
	if( (mod_clock_cycle > 2446) and (mod_clock_cycle <= 2457) ) 	: is_beam = False
	if( (mod_clock_cycle > 2505) and (mod_clock_cycle <= 2542) ) 	: is_beam = False
	if( (mod_clock_cycle > 2590) and (mod_clock_cycle <= 2601) ) 	: is_beam = False
	if( (mod_clock_cycle > 2649) and (mod_clock_cycle <= 2686) ) 	: is_beam = False
	if( (mod_clock_cycle > 2734) and (mod_clock_cycle <= 2745) ) 	: is_beam = False
	if( (mod_clock_cycle > 2793) and (mod_clock_cycle <= 2830) ) 	: is_beam = False
	if( (mod_clock_cycle > 2878) and (mod_clock_cycle <= 2889) ) 	: is_beam = False
	if( (mod_clock_cycle > 2937) and (mod_clock_cycle <= 2974) ) 	: is_beam = False
	if( (mod_clock_cycle > 3022) and (mod_clock_cycle <= 3033) ) 	: is_beam = False
	if( (mod_clock_cycle > 3081) and (mod_clock_cycle <= 3118) ) 	: is_beam = False
	if( (mod_clock_cycle > 3166) and (mod_clock_cycle <= 3177) ) 	: is_beam = False
	if( (mod_clock_cycle > 3225) and (mod_clock_cycle <= 3563) ) 	: is_beam = False
	return is_beam



def is_Run276226_beam(clock_cycle):
	'''
	The beam structure in Run 276226
	'''
	is_beam = True
	mod_clock_cycle = (clock_cycle % 3564)
	# Accidently started at bx 0, sim begins at bx 1 (dont want to rewrite this)
	mod_clock_cycle -= 1
	# Check if current clock cycle has a colliding bunch
	if( (mod_clock_cycle <= 75) )									: is_beam = False
	if( (mod_clock_cycle > 123) and (mod_clock_cycle <= 160) ) 		: is_beam = False
	if( (mod_clock_cycle > 208) and (mod_clock_cycle <= 217) ) 		: is_beam = False
	if( (mod_clock_cycle > 266) and (mod_clock_cycle <= 302) ) 		: is_beam = False
	if( (mod_clock_cycle > 350) and (mod_clock_cycle <= 359) ) 		: is_beam = False
	if( (mod_clock_cycle > 407) and (mod_clock_cycle <= 448) ) 		: is_beam = False
	if( (mod_clock_cycle > 496) and (mod_clock_cycle <= 505) ) 		: is_beam = False
	if( (mod_clock_cycle > 553) and (mod_clock_cycle <= 620) ) 		: is_beam = False
	if( (mod_clock_cycle > 668) and (mod_clock_cycle <= 677) ) 		: is_beam = False
	if( (mod_clock_cycle > 725) and (mod_clock_cycle <= 762) ) 		: is_beam = False
	if( (mod_clock_cycle > 810) and (mod_clock_cycle <= 819) ) 		: is_beam = False
	if( (mod_clock_cycle > 867) and (mod_clock_cycle <= 904) ) 		: is_beam = False
	if( (mod_clock_cycle > 952) and (mod_clock_cycle <= 961) ) 		: is_beam = False
	if( (mod_clock_cycle > 1009) and (mod_clock_cycle <= 1046) ) 	: is_beam = False
	if( (mod_clock_cycle > 1094) and (mod_clock_cycle <= 1103) ) 	: is_beam = False
	if( (mod_clock_cycle > 1151) and (mod_clock_cycle <= 1188) ) 	: is_beam = False
	if( (mod_clock_cycle > 1236) and (mod_clock_cycle <= 1245) ) 	: is_beam = False
	if( (mod_clock_cycle > 1293) and (mod_clock_cycle <= 1342) ) 	: is_beam = False
	if( (mod_clock_cycle > 1390) and (mod_clock_cycle <= 1399) ) 	: is_beam = False
	if( (mod_clock_cycle > 1447) and (mod_clock_cycle <= 1515) ) 	: is_beam = False
	if( (mod_clock_cycle > 1562) and (mod_clock_cycle <= 1571) ) 	: is_beam = False
	if( (mod_clock_cycle > 1619) and (mod_clock_cycle <= 1656) ) 	: is_beam = False
	if( (mod_clock_cycle > 1704) and (mod_clock_cycle <= 1713) ) 	: is_beam = False
	if( (mod_clock_cycle > 1761) and (mod_clock_cycle <= 1798) ) 	: is_beam = False
	if( (mod_clock_cycle > 1846) and (mod_clock_cycle <= 1855) ) 	: is_beam = False
	if( (mod_clock_cycle > 1903) and (mod_clock_cycle <= 1940) ) 	: is_beam = False
	if( (mod_clock_cycle > 1988) and (mod_clock_cycle <= 1997) ) 	: is_beam = False
	if( (mod_clock_cycle > 2045) and (mod_clock_cycle <= 2082) ) 	: is_beam = False
	if( (mod_clock_cycle > 2130) and (mod_clock_cycle <= 2139) ) 	: is_beam = False
	if( (mod_clock_cycle > 2187) and (mod_clock_cycle <= 2236) ) 	: is_beam = False
	if( (mod_clock_cycle > 2284) and (mod_clock_cycle <= 2293) )	: is_beam = False
	if( (mod_clock_cycle > 2341) and (mod_clock_cycle <= 2408) ) 	: is_beam = False
	if( (mod_clock_cycle > 2456) and (mod_clock_cycle <= 2465) ) 	: is_beam = False
	if( (mod_clock_cycle > 2513) and (mod_clock_cycle <= 2550) ) 	: is_beam = False
	if( (mod_clock_cycle > 2598) and (mod_clock_cycle <= 2607) ) 	: is_beam = False
	if( (mod_clock_cycle > 2655) and (mod_clock_cycle <= 2692) ) 	: is_beam = False
	if( (mod_clock_cycle > 2740) and (mod_clock_cycle <= 2749) ) 	: is_beam = False
	if( (mod_clock_cycle > 2797) and (mod_clock_cycle <= 2834) ) 	: is_beam = False
	if( (mod_clock_cycle > 2882) and (mod_clock_cycle <= 2891) ) 	: is_beam = False
	if( (mod_clock_cycle > 2939) and (mod_clock_cycle <= 2976) ) 	: is_beam = False
	if( (mod_clock_cycle > 3024) and (mod_clock_cycle <= 3033) ) 	: is_beam = False
	if( (mod_clock_cycle > 3081) and (mod_clock_cycle <= 3118) ) 	: is_beam = False
	if( (mod_clock_cycle > 3166) and (mod_clock_cycle <= 3175) ) 	: is_beam = False
	if( (mod_clock_cycle > 3223) and (mod_clock_cycle <= 3563) ) 	: is_beam = False
	return is_beam

def is_on_beam(clock_cycle):
	'''
	The default beam structure
	'''
	is_beam = True
	return is_beam


