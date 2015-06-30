set msg to ""
tell application "System Events"
  tell current location of network preferences
		set VPNservice to service "VPN (PPTP)"
		if exists VPNservice then
			set isConnected to connected of current configuration of VPNservice
			if isConnected then
				disconnect VPNservice
				set msg to "Disconnected"
			else
				connect VPNservice
				set isConnectedCheck to false
				#also can try wait util success: repeat until isConnectedCheck
				#now wait in 20s
				set x to 0
				repeat 10 times
					set x to (x + 1)
					set isConnectedCheck to connected of current configuration of VPNservice
					if isConnectedCheck then
						set msg to "Connected success in " & (x * 2) & "s "
						exit repeat
					else
						delay 2
					end if
				end repeat
				if not isConnectedCheck then
					set msg to "Connect fail in 20s"
				end if
			end if
		end if
	end tell
end tell

return text 1 thru -2 of msg