@echo off

vocaloid_announcer_conv^
	--log-level INFO^
	-s source/sources.json^
	-t targets/multirotor.json^
	-t targets/opentx22_system.json^
	convert
