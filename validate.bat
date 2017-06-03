@echo off

echo Missing regions:
vocaloid_announcer_conv^
	-s source/sources.json^
	-t targets/multirotor.json^
	-t targets/opentx21_system.json^
	-t targets/opentx22_system.json^
	list_missing_regions
echo.

echo Unused regions:
vocaloid_announcer_conv^
	-s source/sources.json^
	-t targets/multirotor.json^
	-t targets/opentx21_system.json^
	-t targets/opentx22_system.json^
	list_unused_regions
echo.

echo Filename validation
vocaloid_announcer_conv^
	-s source/sources.json^
	-t targets/multirotor.json^
	-t targets/opentx21_system.json^
	-t targets/opentx22_system.json^
	validate_filenames
echo.
