@echo off

vocaloid_announcer_conv^
	--log-level WARN^
	-s source/sources.json^
	-t targets/multirotor.json^
	-t targets/opentx22_system.json^
	convert
