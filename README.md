# Blog Posts 
- How to get started with Generative Programming.
- Building lenticular art using software
- Rainbow Smoke - Generating art using BFS
	- RGB vs. Lab
	- ColorSpace
	- Breadth First Search

# Deliverables

## Color Space Library
Given an image (or defaults to RGB space), creates a Color Space that given a list of colors, returns the most similar color in that space.

API roughly looks like:

```
# Initialization options
color_space = ColorSpace()
color_space = ColorSpace(size=1000000)
color_space = ColorSpace(images=['./images/images/cool_cat.jpeg'], size=1000000)

# Usage Options
color_space.pop_most_similar_color(colors=[...])
color_space.pop_most_similar_color(colors=[...], threshold=.25)
```

### To-Do for Rainbow Smoke
- Convert current code to API (1-2 day)
	- Handle building image color space
	- Build color_space in ColorSpace (aka. replace ColorSpaceBuilder)
	- pop_most_similar_color should return an Optional[ColorSpaceItem]
	- Replace color_diff usage with color_math?
	- pop_most_similar_color should just expect a 3 part tuple?
- Make sure it works with python2.7 and python3 (1 day)
	- Publish and make sure it works in current project.

### Open Questions
- Should we be using Numpy arrays for this kind of thing?
- What type should the colors be? Do we publish a type as well?
- What is the runtime of each call? Is removing each time the right way?

## Lenticular Art
1. Intro to Lentricular Art
2. Original High-level approach
  2.1 Cool animation
3. Getting position in the room
  3.1 Face detection
4. Communicating face's location to processing
5. Leverage position of face to render the appropriate pixels
6. Final result?

### To-Do
- Cool animation?
