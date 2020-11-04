let ac, as;
let b1, b2, b3;
let startTime;
let gameTime;
let lastclick;
let wait;

function setup() {
  getAudioContext().suspend();
  createCanvas(windowWidth, windowHeight);
  background(25, 20, 20, 255);
  frameRate(50);
  b1 = new button(width / 2, 7 * height / 8, getButtonR(), color(220, 60, 60), color(25, 20, 20, 10), "", color(200));
  b2 = new button(b1.x - b1.r * 3, b1.y, b1.r, color(20, 60, 220), color(25, 20, 20, 10), "-", color(200));
  b3 = new button(b1.x + b1.r * 3, b1.y, b1.r, color(20, 60, 220), color(25, 20, 20, 10), "+", color(200));
  gameTime = 3000;
  lastclick = 0;
  wait = 0;
  as = -1;
  print("infectoDoppler: v0.510 beta");
}

function draw() {
  processTriggers();
  background(25, 20, 20);
  b1.display(mouseX, mouseY);
  b2.display(mouseX, mouseY);
  b3.display(mouseX, mouseY);
  if (as != -1) {
    ac.display();
  }
}

function mousePressed() {
  if (500 < millis() - lastclick) {
    if (b1.contains(mouseX, mouseY)) {
      if (as === -1) {
        userStartAudio();
        ac = new audiocontrol(0.9);
        as = 0;
      } else if (as === 0) {
        startTime = millis();
        ac.record();
        as = 1;
      }
    } else if (b2.contains(mouseX, mouseY)) {
      ac.decreaseInputLevel();
    } else if (b3.contains(mouseX, mouseY)) {
      ac.increaseInputLevel();
    }
    lastclick = millis();
  }
}

function keyPressed() {
  ac.play();
}

function processTriggers() {
  if (millis() > startTime + gameTime && as === 1) {
    ac.stop();
    as = 2;
    background(255);
  } else if (millis() > startTime + gameTime + wait && as === 2) {
    try {
      ac.save();
      print("Saving audio...");
      as = 0;
    } catch {
      wait += 250;
      print("Error: Imposible to save audio...")
    }
  }
}

function getButtonR() {
  if (width > height) {
    return round(height / 25);
  } else {
    return round(width / 20);
  }
}
