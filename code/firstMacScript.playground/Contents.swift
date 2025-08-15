import UIKit

class Person{
    var name:String?
    var age:Int?
}

var p = Person()
p.name = "jo"

if let actualName = p.name{
    print(actualName + " is amazing")
}

class Dog{
    var breed:String
    var name:String
    
    init(){
        breed = "labrador"
        name = "buddy"
    }
    init(breed:String, name:String){
        self.breed = breed
        self.name = name
    }
}


var myArr = ["balls", "nuts","cashews"]
//empty Stirng
var strings = [String]()


var dict = Dictionary<Int,String>()
var names = ["Andre", "Robert", "Henry", "Edwin", "Anahid", "David", "John"]



for _ in 1...10{
    let randomInt = Int.random(in: 100000000...999999999)
    let randomName = names[Int.random(in: 0...names.count-1)]
    dict[randomInt] = randomName
}

for (id, name) in dict{
    print("\(name)'s ID # is: \(id)")
    
}
