'''
Timeline widget

    Design:
        - The timeline contains time dependent data and allows scrolling between temporal views
        - The time dependent data is graphed and displayed as a background layer
        - Any type of time dependent graph should be able to be displayed
            - line graph, density, etc
        - Multiple graphs can be displayed at a time
        - On the left side is displayed the upper value and lower value for the data displayed by graph
            - Additional two values are displayed for upper and lower intensity when relevant

    Functionality:


    User interaction:
        Temporal interface:
            - user is able to drag a timeline-cursor across the timeline
                - mouse left button dragging
                - ctrl left/right keys for small step
                - left/right keys for normal step
                - shift left/right keys for large step
            - user is able to zoom in and out
                - mouse wheel
                - ctrl +, ctrl -
            - user is able to pan view via mouse left button dragging
            - user is able to double click to make the timeline-cursor jump to that point
            - user is able to select a range via mouse right button dragging

        Graph interface:
            - user is able to mouse over a point on graph to see value
            - user is able to resize y-axis
                - mouse dragging
                - mouse wheel
            - user is able to click on a point on graph to highlight a point
            - user is able to double click a point on graph to make the timeline-cursor jump to that point
            - user is able to select a range of data via mouse right button dragging
                - holding ctrl allows user to perform inclusive selection
                - holding shift allows user to perform exclusive selection
            - displayed graph transparency can be adjusted via spinbox

        Graph cycler interface:
            - TODO

    Output:


'''