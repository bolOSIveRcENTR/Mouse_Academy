function stru = InitializeWindow()

% Clear the workspace and the screen

close all;

% Setup PTB with some default values
PsychDefaultSetup(2);

% Set the screen number to the external secondary monitor if there is one
% connected
screens = Screen('Screens')
screenNumber = max(screens);

% Define black, white and grey
white = WhiteIndex(screenNumber);
grey = white / 2;

% Skip sync tests for demo purposes only
Screen('Preference', 'SkipSyncTests', 2);

% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2,...
    [], [],  kPsychNeed32BPCFloat);


stru = struct('Window', window, 'WindowRect', windowRect, 'Grey', grey);
return;
end
