let state;
let b1, b2, lastclick;
let g;
let da;

function setup() {
  getAudioContext().suspend();
  createCanvas(windowWidth, windowHeight);
  background(25, 20, 20, 255);
  frameRate(50);
  state = -1;
  lastclick = 0;
  b1 = new button(width / 3, height / 8, this.getButtonR(), color(220,60, 60), color(25, 20, 20, 10), "", color(0));
  b2 = new button(2 * width / 3, height / 8, this.getButtonR(), color(20, 60, 220), color(25, 20, 20, 10), "", color(0));
  g = new gravity(1, 1, 25, true);
  print("infectoDoppler: example v.0.95");
}

function draw() {
  background(25, 20, 20, 10);
  b1.display(mouseX, mouseY);
  b2.display(mouseX, mouseY);
  switch (state) {
    case 0:
      g.display();
      break;
    case 1:
      da.updateDopplerFactor(g.stars[0].p, g.asteroids[0].p);
      da.updateOscillator();
      g.display();
      break;
  }
}

function mousePressed() {
  if (500 < millis() - lastclick) {
    if (b1.contains(mouseX, mouseY)) {
      switch (state) {
        case -1:
          userStartAudio();
          da = new dopplerAudio(350, 6);
					g.play();
          state = 0;
          break;
        case 0:
          da.play();
          state = 1;
          break;
        case 1:
          da.stop();
          state = 0;
          break;
      }
    } else if (b2.contains(mouseX, mouseY)) {
      g.asteroids[0].reset();
    }
    lastclick = millis();
  }
}

function getButtonR() {
  if (width > height) {
    return round(height / 25);
  } else {
    return round(width / 20);
  }
}
