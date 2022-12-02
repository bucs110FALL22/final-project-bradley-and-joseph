:warning: Everything between << >> needs to be replaced (remove << >> after replacing)
# CS110 Project Proposal
# << Project Title >>
## CS 110 Final Project
### << Semester, Year >>
### [Assignment Description](https://docs.google.com/document/d/1H4R6yLL7som1lglyXWZ04RvTp_RvRFCCBn6sqv-82ps/edit?usp=sharing)

<< [repl](#) >> https://replit.com/join/awmmbraijp-josephmichaud1

<< [link to demo presentation slides](#) >>

### Team: << Bradley and Joseph >>
#### << Bradley and Joseph >>

***

## Project Description

<< Give an overview of your project >>
# We aim to create a gimmicky rhythm game with mechanics similar to games like Dance Dance Revolution and Guitar Hero with tracks, notes, and terminals for the notes that respond to button inputs. What would make our game different is that the tracks are arranged in a cross pattern with the notes converging in the center. To keep it from being too overwhelming, only the left and right tracks are active at a time and the player has the ability to rotate the order of the terminals. It's admittedly difficult to explain, but visually a simple concept, and simple concepts with lots of applications make for potentially difficult but enjoyable gameplay.
***    

## User Interface Design

- **Initial Concept**
  - << A wireframe or drawing of the user interface concept along with a short description of the interface. You should have one for each screen in your program. For example, if your program has a start screen, game screen, and game over screen, you should include a wireframe / screenshot / drawing of each one and a short description of the components. >>
    
    
- **Final GUI**
  - << You should also have a screenshot of each screen for your final GUI >>

***        

## Program Design

* Non-Standard libraries
    * << You should have a list of any additional libraries or modules used (pygame, request) beyond non-standard python. 
         For each additional module you should include
         - url for the module documentation
         - a short description of the module >>
* Class Interface Design
    * << A simple drawing that shows the class relationships in your code (see below for an example). This does not need to be overly detailed, but should show how your code fits into the Model/View/Controller paradigm. >>
        * ![class diagram](assets/class_diagram.jpg) 
* Classes
    * Button: color, orientation, position, active, on
      * init: creates a button in the desired position, with a designated
      * pressed: called when the button is pressed, changes the active variable
      * rotate: when the record is rotated, this will change the orientation of the button
      * draw: used to draw the buttons

    * Record: surface, height and width, list of buttons
      * init: Creates the record in which the buttons will be drawn on
      * spin: Spins the record and then tells the buttons to change position
      * draw: used to draw the record and tell the buttons to draw themselves

## Project Structure and File List

The Project is broken down into the following file structure:

* main.py
* src
  *  main
  *  var
  *  colors
  *  Objects:
    *  Record
    *  Button
* assets
    * << all of your media, i.e. images, font files, etc, should go here) >>
* etc
    * << This is a catch all folder for things that are not part of your project, but you want to keep with your project >>

***

## Tasks and Responsibilities 

   * Outline the team member roles and who was responsible for each class/method, both individual and collaborative.
  #Bradley did the art work and game logic
  #Joseph did the menu logic and music sounds
## Testing

* << Describe your testing strategy for your project. >>
  #would run the program a lot if there was a bug we would fix it
## ATP

| Step                 |Procedure             |Expected Results                   |
|----------------------|:--------------------:|----------------------------------:|
|  1                   | start the program |menu window should open  |
|  2                   | click play  | should open a menu for easy or hard mode    |
|3|click easy or hard|should open the main game on the selected mode|
|4|click the notes when they move into the buttons using A or D|should make the notes disabpear|
|5|if the notes are on a diffrent color not assigend to A or D click space to change the color rotation|should spin the record|                     

