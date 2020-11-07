let state;
let b1, b2, b3;
let ac;
let sn, an, gc, isFixed, miclevel, micamp;
let g;
let startTime, gameTime, pause, wait;
let lastclick;

function setup() {
  getAudioContext().suspend();
  createCanvas(windowWidth, windowHeight);
  background(25, 20, 20, 255);
  frameRate(50);
  config = getURLParams();
  startConfig(config);
  state = -2;
  lastclick = 0;
	pause = 1200;
	wait = 250;
  buildButtons();
  g = new gravity(sn, an, gc, isFixed);
  print("infectoDoppler player's guide v0.91");
}

function draw() {
	print(state + " " + startTime);
  background(25, 20, 20, 10);
	if (state === 2 || state === 3) {
		g.display();
		processTriggers();
	} else if (state === 1) {
		g.display();
		pauseRelease();
	} else if (state === 0) {
		g.display();
		b1.display(mouseX, mouseY);
	} else if (state === -1) {
		ac.display();
		b1.display(mouseX, mouseY);
		b2.display(mouseX, mouseY);
		b3.display(mouseX, mouseY);
	} else if (state === -2) {
		b1.display(mouseX, mouseY);
	}
}

function mousePressed() {
  if (500 < millis() - lastclick) {
    if (b1.contains(mouseX, mouseY)) {
      switch (state) {
				case 0:
          background(25, 20, 20, 255);
          startTime = millis();
          state = 1;
          break;
				case -2:
          background(25, 20, 20, 255);
          userStartAudio();
          ac = new audiocontrol(micamp);
          if (miclevel) {
            state = -1;
          } else {
            state = 0;
          }
          break;
        case -1:
          background(25, 20, 20, 255);
					startTime = millis();
          state = 0;
          break;
      }
    } else if (b2.contains(mouseX, mouseY) && state === -1) {
      ac.decreaseInputLevel();
    } else if (b3.contains(mouseX, mouseY) && state === -1) {
      ac.increaseInputLevel();
    }
    lastclick = millis();
  }
}

function pauseRelease() {
	if (millis() > startTime + pause && state === 1) {
		g.play();
		ac.record();
		startTime = millis();
		state = 2;
	}
}

function processTriggers() {
  if (millis() > startTime + gameTime && state === 2) {
    ac.stop();
    g.stop();
    state = 3;
    background(200, 20, 60);
  } else if (millis() > startTime + gameTime + wait && state === 3) {
    try {
      ac.save();
      print("Saving audio...");
      state = 0;
			gameTime = getGameTime();
      background(25, 20, 20, 255);
    } catch {
      wait += 250;
      print("Error: Imposible to save audio...")
    }
  }
}

function buildButtons() {
  b1 = new button(width / 2, 7 * height / 8, getButtonR(), color(220, 60, 60), color(25, 20, 20, 10), "", color(200));
  b2 = new button(b1.x - b1.r * 3, b1.y, b1.r, color(20, 60, 220), color(25, 20, 20, 10), "-", color(200));
  b3 = new button(b1.x + b1.r * 3, b1.y, b1.r, color(20, 60, 220), color(25, 20, 20, 10), "+", color(200));
}

function getButtonR() {
  if (width > height) {
    return round(height / 25);
  } else {
    return round(width / 20);
  }
}

function getGameTime(){
	return 6795 + round(random(4181));
}

function startConfig(config) {
  gameTime = getGameTime();
  let number = Number(config.sn);
  if (typeof(number) === "number" && Number.isInteger(number)) {
    sn = number;
  } else {
    sn = 3;
  }
  number = Number(config.an);
  if (typeof(number) === "number" && Number.isInteger(number)) {
    an = number;
  } else {
    an = 1;
  }
  number = Number(config.gc);
  if (typeof number === "number" && Number.isFinite(number)) {
    gc = number;
  } else {
    gc = 10;
  }
  let string = config.fix;
  if (typeof string === "string" && string === "true") {
    isFixed = true;
  } else {
    isFixed = false;
  }
  string = config.mic;
  if (typeof string === "string" && string === "false") {
    miclevel = false;
  } else {
    miclevel = true;
  }
  number = Number(config.amp);
  if (typeof number === "number" && Number.isFinite(number)) {
    micamp = number;
  } else {
    micamp = 0.9;
  }
}
