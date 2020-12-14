class asteroid {

  constructor(v, s, m, fix) {
    this.v = v;
    this.r = this.getRadious(s);
    this.ang = TWO_PI / this.v;
    this.rn = [];
    for (let p = 0; p < v; p ++) {
      this.rn[p] = random(this.r / 4);
    }
    this.ar = 0;
    this.m = m;
    this.isFixed = fix;
    if (this.isFixed === true) {
      this.p = createVector(width / 4, height / 2);
      this.s = createVector(0, random(4));
    } else {
      this.p = createVector(this.getCoordinate(width), this.getCoordinate(height));
      this.s = this.getInitSpeed();
    }
    this.a = createVector(0, 0);
    this.color = this.getColor();
  }

  display() {
    push();
    translate(this.p.x, this.p.y);
    rotate(this.ar);
    fill(this.color);
    noStroke();
    this.shape();
    pop();
  }

  update(a) {
    this.a.set(a);
    this.s.add(this.a);
    this.p.add(this.s);
    this.getRotation(this.a, this.s);
  }

  shape() {
    beginShape();
    for (let p = 0; p < this.v; p ++) {
      let angle = this.ang * p;
      let vx = cos(angle) * this.r + this.rn[p];
      let vy = sin(angle) * this.r + this.rn[p];
      vertex(vx, vy);
    }
    endShape(CLOSE);
  }

  getRotation(f, a) {
    let angle = a.angleBetween(f) / 25;
    return this.ar += angle;
  }

  reset(){
    if (this.isFixed === true) {
      this.p.set(width / 4, height / 2);
      this.s.set(0, random(4));
    } else {
      this.p.set(this.getCoordinate(width), this.getCoordinate(height));
      this.s.set(this.getInitSpeed());
    }
  }

  getColor() {
    let r = second() * 2 + 35 + random(65);
    let g = hour() * 5 + 35 + random(65);
    let b = minute() * 2 + 65 +random(35);
    return color(r, g, b);
  }

  getCoordinate(limit) {
    let l = limit / 5;
    return l + random(l) + this.getZone(l);
  }

  getZone(l) {
    if (random() < 0.5) {
      return 0;
    } else {
      return 2 * l;
    }
  }

  getRadious(s) {
    if (width < height) {
      return width * 0.02 * s;
    } else {
      return height * 0.015 * s;
    }
  }

  getInitSpeed() {
    let speed = createVector(0, 0);
    let s = random(1.5);
    if (width < height) {
      speed.set(s, s + random(1.5));
    } else {
      speed.set(s + random(1.5), s);
    }
    return speed;
  }

	setSpeed(x, y) {
		this.s.set(p5.Vector.sub(createVector(x, y), this.p));
		this.s.setMag(this.s.mag()/50);
	}

}
