class gravity {

  constructor(sn, an, g, fix) {
    this.state = 0;
    this.sn = sn;
    this.an = an;
    this.G = g;
		this.C = createVector(width / 2, height / 2);
		this.Cm = 0.25;
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
				this.getStarAcceleration(this.C, this.stars[i]);
				this.stars[i].setInitSpeed(this.C);
      }
    }
  }

  buildAsteroids() {
    for (let i = 0; i < this.an; i ++) {
      if (this.isFixed === true) {
        this.asteroids.push(new asteroid(7, 1, 0.5, true));
      } else {
        this.asteroids.push(new asteroid(7, 1, 0.5, false));
      }
    }
  }

  display() {
    if (this.state != 0) {
      this.getStarsAccelerations();
      this.getAsteroidsAttractions()
    }
    for (let i = 0; i < this.sn; i ++) {
      this.stars[i].display();
    }
    for (let i = 0; i < this.an; i ++) {
      this.asteroids[i].display();
    }
  }

  getStarsAccelerations() {
    for (let i = 0; i < this.sn; i ++) {
			this.getStarAcceleration(this.C, this.stars[i]);
    }
  }

  getStarAcceleration(center, object) {
    let a = p5.Vector.sub(center, object.p);
    let dSq = constrain(a.magSq(), 20, 800);
    let mag = this.G * this.Cm / dSq;
    a.setMag(mag);
		object.update(a);
  }

  getAsteroidsAttractions() {
    for (let a = 0; a < this.an; a ++) {
      for (let s = 0; s < this.sn; s ++) {
        this.getAsteroidAcceleration(this.stars[s], this.asteroids[a]);
      }
    }
		for (let a = 0; a < this.an; a ++) {
      for (let s = 1; s < this.an; s ++) {
        this.getAsteroidAcceleration(this.asteroids[(a + s)%this.an], this.asteroids[a]);
      }
    }
  }

  getAsteroidAcceleration(attractor, object) {
    let a = p5.Vector.sub(attractor.p, object.p);
    let dSq = constrain(a.magSq(), 0.01, 750);
    let mag = this.G * attractor.m / dSq;
    a.setMag(mag);
    object.update(a);
  }

	setAsteroidsSpeed(x, y) {
		for (let i = 0; i < this.an; i ++) {
      this.asteroids[i].setSpeed(x, y);
    }
	}

	getStarPosition(n) {
		return this.stars[n].p;
	}

	getAsteroidPosition(n) {
		return this.asteroids[n].p;
	}

	isAsteroidInCanvas(n) {
		if (this.asteroids[n].p.x > width || this.asteroids[n].p.x < 0) {
			return false;
		} else if (this.asteroids[n].p.y > height || this.asteroids[n].p.y < 0) {
			return false;
		} else {
			return true;
		}
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
			this.getStarAcceleration(this.C, this.stars[i]);
			this.stars[i].setInitSpeed(this.C);
    }
    for (let i = 0; i < this.an; i ++) {
      this.asteroids[i].reset();
    }
  }

}
