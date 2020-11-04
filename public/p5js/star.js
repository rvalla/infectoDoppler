class star {

  constructor(fix) {
    this.m = 1.25 + random(0.75);
    this.color = this.getColor();
    this.d = this.getDiameter();
    this.isFixed = fix;
    if (this.isFixed === true) {
      this.p = createVector(width / 2, height / 2);
      this.s = createVector(0, 0);
    } else {
      this.p = createVector(this.getCoordinate(width), this.getCoordinate(height));
      this.s = this.getInitSpeed();
    }
    this.a = createVector(0, 0);
  }

  display() {
    push();
    translate(this.p.x, this.p.y);
    fill(this.color);
    noStroke();
    ellipseMode(CENTER);
    ellipse(0, 0, this.d, this.d);
    pop();
  }

  update(f) {
    this.s.set(p5.Vector.div(f, this.m));
    this.p.add(this.s);
  }

  reset() {
    if (this.isFixed === true) {
      this.p.set(width / 2, height / 2);
      this.s.set(0, 0);
    } else {
      this.p.set(this.getCoordinate(width), this.getCoordinate(height));
      this.s.set(random(0.05), random(0.05));
    }
  }

  getDiameter() {
    if (width < height) {
      return this.m * width * 0.05;
    } else {
      return this.m * height * 0.0375;
    }
  }

  getColor() {
    let r = 200 + random(50);
    let g = 180 + random(75);
    let b = second();
    return color(r, g, b);
  }

  getCoordinate(limit) {
    let l = limit / 4;
    return 1.5 * l + random(l);
  }

  getInitSpeed() {
    let speed = createVector(0, 0);
    let s = random(0.25);
    if (width < height) {
      speed.set(s, s + random(0.25));
    } else {
      speed.set(s + random(0.25), s);
    }
    return speed;
  }

}
