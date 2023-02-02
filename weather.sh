#!/bin/fish

# set --local options 'h/help' 'n/count=!_validate_int --min 1'
# set --local options 'f/feels'
# argparse $options -- $argv

curl -sm10 "https://wttr.in/Dublin?format=%c;%t;%f;%S;%s;%h;%w;%p;%P;%C;%m" | read -d \; condition temperature feels sunrise sunset humidity wind precipitation pressure condition_desc moonphase

set feels_display (string trim --chars=+C -- $feels)
set temp_display (string trim --chars=+C -- $temperature)
set sunrise (string sub --length 5 -- $sunrise)
set sunset (string sub --length 5 -- $sunset)

# if set --query _flag_feels
#     echo $feels "| size=16 color=#7777bb"
#     exit 0
# end

# if string match x$temp_display x$feels_display
#     # the prefix 'x' in this case is to avoid negative temperatures triggering an option/error
#     set feels_display "="
# end


if string match -rq '^feels\.' (basename (status current-filename))
    # if [ (basename (status current-filename)) = "feels.*" ]
    echo $feels
    exit 0
else
    echo -n "$condition_desc $temp_display($feels_display)"
    # set suffix "| size=18 color=white font='Patrick Hand'"

    # echo '---'
    # echo "actual temp: " $temperature $suffix
    # echo "feels like: " $feels $suffix
    # echo "sunrise: " $sunrise $suffix
    # echo "sunset: " $sunset $suffix
    # echo '---'
    # echo "humidity: " $humidity $suffix
    # echo "wind: " $wind $suffix
    # echo "precipitation: " $precipitation $suffix
    # echo "pressure: " $pressure $suffix
    # echo "conditions: " $condition_desc $suffix
    # echo '---'
    # echo "moon: " $moonphase $suffix
    # echo '---'
    # end

    # echo "🌊 tides at Sandymount strand:" "$suffix"
    # ~/bin/sandymount | while read line
    # echo $line $suffix
end

# echo '---'


# echo (basename (status current-filename))
