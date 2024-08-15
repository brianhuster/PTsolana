const express = require('express');
const path = require('path');
const app = express();
const PORT = 5000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'view'));

app.use(express.static(path.join(__dirname, 'public')));

app.use(express.json())
app.use(express.urlencoded({ extended: true }));

// const routes = require('./routes');
const { info } = require('console');
// app.use('/', routes);

async function getJSON(link){
    try {
        const response = await fetch(link);
        if (response.status !== 200) {
            alert("Error");
        } else {
            const x = await response.json();
            return x;
        }
    }
    catch (error) {
        throw new Error("Cannot connect to " + link);
        alert("Cannot connect to "+link);
    }
}

async function getAllClasses(){
    let classes = await getJSON("http://localhost:8000/get-all-gym-classes-data");
    let results = [];
    
    classes.data.forEach((classData) => {
        class_object = {
            name: classData.name,
            info: classData.info,
            price: classData.price
        };
        results.push(class_object);
    });
    return results;
}

app.get('/', (req, res) => {
    getAllClasses().then((classes) => {
        res.render('index', { title: 'Home', classes: classes });
    });
});

app.get('/index', (req, res) => {
    getAllClasses().then((classes) => {
        res.render('index', { title: 'Home', classes: classes });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
