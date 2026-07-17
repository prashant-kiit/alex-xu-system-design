interface IEngine {
    public void start();
}

class Engine implements IEngine {
    public void start() {
        System.out.println("Engine starting");
    }
}

class PetrolEngineAdapter implements IEngine {
    private IEngine engine = new Engine();
    
    // adapter pattern 
    // if enriched with control access then it is proxy pattern 
    public void start() {
        System.out.println("Petrol Engine starting");
        this.engine.start();
    }
}

class Wheel {
    public void spin() {
        System.out.println("Wheels spinning");
    }
}

class Weapon {
    public void fire() {
        System.out.println("Weapons firing");
    }
}

interface IRobot {
    public void move();
}

interface ICar {
    public void move();
}

class Robot implements IRobot {
    private IEngine engine;
    private Wheel wheel;
    private Weapon weapon;

    Robot(IEngine engine, Wheel wheel, Weapon weapon) {
        // composite pattern
        this.engine = engine;
        this.wheel = wheel;
        this.weapon = weapon;
    }

    // faccade pattern
    public void move() {
        this.engine.start();
        this.wheel.spin();
        this.weapon.fire();
    }
}

class RobotDecorator implements IRobot {
    private IRobot robot;

    RobotDecorator(IRobot robot) {
        // composite pattern
        this.robot = robot;
    }

    public void move() {
        System.out.println("Move Slower");
        this.robot.move();
        System.out.println("Move Faster");
    }
}

class Car implements ICar {
    private IEngine engine;
    private Wheel wheel;
    private Weapon weapon;

    Car(IEngine engine, Wheel wheel, Weapon weapon) {
        // composite pattern
        this.engine = engine;
        this.wheel = wheel;
        this.weapon = weapon;
    }

    // faccade pattern
    public void move() {
        this.engine.start();
        this.wheel.spin();
        this.weapon.fire();
    }
}

class CarDecorator implements ICar {
    private ICar car;

    CarDecorator(ICar car) {
        // composite pattern
        this.car = car;
    }

    public void move() {
        System.out.println("Move Slower");
        this.car.move();
        System.out.println("Move Faster");
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("Structural Design Pattern");
        // bridge pattern
        IEngine engine = new PetrolEngineAdapter();
        Wheel wheel = new Wheel();
        Weapon weapon = new Weapon();
        // bridge pattern
        IRobot robot = new Robot(engine, wheel, weapon);
        ICar car = new Car(engine, wheel, weapon);
        // decorator pattern
        RobotDecorator robotDecorator = new RobotDecorator(robot);
        CarDecorator carDecorator = new CarDecorator(car);
        robotDecorator.move();
        carDecorator.move();
    }
}
