Serial Protocol Design
======================

When sending bytes to Arduino from Python, the Python side needs to
wait for readiness before sending anything, and could also benefit
from waiting frame-by-frame.

Initial Brainstorming
---------------------

- need initial "arduino is ready": no send before this
- acknowledgment of bytes received? (why? debugging possibly)
- frame done signal: prevent Python from sending new data before Arduino is ready
- other stuff?

Useful outcomes:
- ability to measure timing
- prevent overrun

Data transfer rate: how fast can 9600 baud transfer 896 bytes?
896 bytes divided by 9600 bytes / sec = 0.093 repeating (93 and 1/3 milliseconds)

Idea: only send from Python when Arduino asks for it. Python is an on-demand server for image bytes.

Python should always have a buffer ready to send to Arduino, so that it can respond immediately.

First Draft Design
------------------

Python reads repeatedly with small delay (10ms?) waiting for commands from Arduino.

Commands should be simple, human-readable but short, like "READY", "FRAME", or "DEBUG".

Command palette:
- READY: Arduino is online. Do not send any bytes before this.
- FRAME _N_: Arduino is ready for a single image frame. Send N bytes and then go back to waiting.
- DEBUG _message_: Arduino has debug data. Read until newline and collect that message for human consumption.
- END: Arduino is done. Stop sending bytes forever.

When Arduino fails to get a frame within a certain time (500ms?),
it should assume that Python is gone, and blank the screen.

### Python Side

Infinite `while` loop after initialization. Check data for command: if no command is found, refresh the
ready-to-send buffer. If a command _is_ found, and the command is "FRAME" then send the image.
