class gravity {

  constructor(sn, an, g, fix) {
    this.state = 0;
    this.sn = sn;
    this.an = an;
    this.G = g;
    this.stars = [];
    this.asteroids = [];
    this.isFixed = fix;
    this.buildStars();
    this.buildAsteroids();
  }

  buildStars() {
    for (let i = 0; i < this.sn; i ++) {
      if (this.isFixed === true) {
        this.stars.push(new star(true));
      } else {
        this.stars.push(new star(false));
      }
    }
  }

  buildAsteroids() {
    for (let i = 0; i < this.an; i ++) {
      if (this.isFixed === true) {
        this.asteroids.push(new asteroid(7, 1, 0.1, true));
      } else {
        this.asteroids.push(new asteroid(7, 1, 0.1, false));
      }
    }
  }

  display() {
    if (this.state != 0) {
      this.getStarsAttractions();
      this.getAsteroidsAttractions()
    }
    for (let i = 0; i < this.sn; i ++) {
      this.stars[i].display();
    }
    for (let i = 0; i < this.an; i ++) {
      this.asteroids[i].display();
    }
  }

  getStarsAttractions() {
    for (let i = 0; i < this.sn; i ++) {
      for (let s = 1; s < this.sn; s ++) {
        this.getStarAttraction(this.stars[(i + s)%this.sn], this.stars[i]);
      }
    }
  }

  getStarAttraction(attractor, object) {
    let f = p5.Vector.sub(attractor.p, object.p);
    let dSq = constrain(f.magSq(), 20, 800);
    let mag = this.G * (object.m * attractor.m) / dSq;
  //  if ()
    f.setMag(mag);
    object.update(f);
  }

  getAsteroidsAttractions() {
    for (let a = 0; a < this.an; a ++) {
      for (let s = 0; s < this.sn; s ++) {
        this.getAsteroidAttraction(this.stars[s], this.asteroids[a]);
      }
    }
  }

  getAsteroidAttraction(attractor, object) {
    let f = p5.Vector.sub(attractor.p, object.p);
    let dSq = constrain(f.magSq(), 10, 500);
    let mag = this.G * (object.m * attractor.m) / dSq;
    f.setMag(mag);
    object.update(f);
  }

  play() {
    this.state = 1;
  }

  stop() {
    this.state = 0;
  }

  reset() {
    for (let i = 0; i < this.sn; i ++) {
      this.stars[i].reset();
    }
    for (let i = 0; i < this.an; i ++) {
      this.asteroids[i].reset();
    }
  }

}
