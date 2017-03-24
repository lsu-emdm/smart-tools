
				// The not fun way to deal with the dictionary...
function bang()
{	
	// The dictionary object loaded...
	var dict = new Dict("Test");
		// get an item from the dictionary
	var foo = dict.get("foo");
		post("foo = " + foo + "\n");
		// get an array from the dictionary
	var fooArray = dict.get("fooArray")
		post("length of fooArray = " + fooArray.length + "\n")
}

			// The fun javascripty way to deal with the dictionary... :)
function dictionary(name) {
   	var d = new Dict(name);
		// the dictionary!
		post("d = " + d + "\n");
		
		// Make it into a JSON object!
   	var jsd = JSON.parse(d.stringify());
			// How many items are in the new jason obj.
		post("length of jsd = " + Object.keys(jsd).length + "\n")
		post("Keys: ", Object.keys(jsd)+ "\n");
		post("Individual item fooArray[0].baz: ", jsd.fooArray[0].baz+ "\n");
	
	// reading through all of the keys in the json.
	for (var key in jsd) {
		if (jsd.hasOwnProperty(key)) {
			post(key + " -> " + jsd[key] + "\n");
		}
	}
		// recursively reading through all properties...
	walk(jsd);
}

// recursively reading through all properties...
function walk(obj) {
	for (var key in obj) {
		if (obj.hasOwnProperty(key)) {
			var val = obj[key];
			if (typeof val == "object") {
                	walk(val); 
			} else {
				post(key + " -> " + val + "\n");
			}
		}
	}
}
walk.local = 1;


	// Send in a string version of a JSON Object and iterate over it...
function walkString(str) {
	post(str);
	obj = JSON.parse(JSON.stringify(eval("(" + str + ")"))); 
	post(obj + "\n");
	
	function walkin(obj) {
		for (var key in obj) {
			if (obj.hasOwnProperty(key)) {
				var val = obj[key];
				if (typeof val == "object") {
                	walkin(val); 
				} else {
					post(key + " -> " + val + "\n");
				}
			}
		}
	}
	walkin(obj);
}
