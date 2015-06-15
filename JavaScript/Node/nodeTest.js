console.log("Hello, Cruel World!");

console.log("\n");


var Person = function (firstName) {
  this.firstName = firstName;
  console.log('Person instantiated');
};

var person1 = new Person('Alice');
var person2 = new Person('Bob');

// Show the firstName properties of the objects
console.log('person1 is ' + person1.firstName); // logs "person1 is Alice"
console.log('person2 is ' + person2.firstName); // logs "person2 is Bob"



function Person(firstName) {
  this.firstName = firstName;
  console.log('Person instantiated');
};

var person1 = new Person('Alice');
var person2 = new Person('Bob');

// Show the firstName properties of the objects
console.log('person1 is ' + person1.firstName); // logs "person1 is Alice"
console.log('person2 is ' + person2.firstName); // logs "person2 is Bob"


function Car() {
}

Car.prototype.go = function() {
    console.log("Vroom vroom " + this.numDoors);
};

Car.prototype.numDoors = 2;

var myCar = new Car();
myCar.go();