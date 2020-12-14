let state;
let g;
let sn, an, gc, isFixed;
let lastclick;

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(25, 20, 20, 255);
  frameRate(50);
  config = getURLParams();
  startConfig(config);
  state = 0;
  lastclick = 0;
  g = new gravity(sn, an, gc, isFixed);
  print("infectoDoppler gravity test: v0.95");
}

function draw() {
  background(25, 20, 20, 10);
  g.display();
}

function mousePressed() {
  if (500 < millis() - lastclick) {
    switch (state) {
      case 0:
        g.play();
        state = 1;
        break;
      case 1:
        g.stop();
        g.reset();
        state = 0;
        break;
    }
    lastclick = millis();
  }
}

function startConfig(config) {
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
    an = 3;
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
}
