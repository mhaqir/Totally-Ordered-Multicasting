#!/bin/bash

osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/F_R.py --nc 5 \""
osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/main.py --id sequencer \""
osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/main.py --id c1 --com /Users/mohamadhaghir/Dis_HW4/test/test1.txt -o /Users/mohamadhaghir/Dis_HW4/test \""
osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/main.py --id c2 --com /Users/mohamadhaghir/Dis_HW4/test/test2.txt -o /Users/mohamadhaghir/Dis_HW4/test \""
osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/main.py --id c3 --com /Users/mohamadhaghir/Dis_HW4/test/test3.txt -o /Users/mohamadhaghir/Dis_HW4/test \""
osascript -e "tell application \"Terminal\" to do script \"python /Users/mohamadhaghir/Dis_HW4/main.py --id c4 --com /Users/mohamadhaghir/Dis_HW4/test/test4.txt -o /Users/mohamadhaghir/Dis_HW4/test \""
