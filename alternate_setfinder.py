def delay(func):
	""" decorator to delay"""
	def wrapper(*args):
		time.sleep(1)
		func(*args)
	return wrapper
"""
# This is the set finding using a hashmap --> n**2 complexity
@delay
def process_Screen():
	driver.save_screenshot('allsets.png')
	allsets = cv2.imread('allsets.png')


	# print("Got the  whole screenshot")
	for idx, button in enumerate(buttons):
		if cards_list[idx] is None: # update only the cards
			# Crop the image
			location, size = button.location, button.size
			x, y, h, w = location['x'], location['y'], size['height'], size['width']
			cardimg = allsets[y:y+h, x:x+w]
			
			img_path = f"button{idx}.png"
			cv2.imwrite(img_path, cardimg) # Debug check
			img = cardimg, cv2.cvtColor(cardimg, cv2.COLOR_BGR2GRAY) # convert to grayscale
			
			# print("just wrote button", idx)
			if idx == cards:
				print(idx, cards, "breaking!")
				blank_button_idx = idx
				break
			else:
				cards_list[idx] = create_Card(img_path, KERNEL)
				key = cards_list[idx].hash()
				

				if key not in cards_map: # add the value in the map
					cards_map[key] = [idx]
					print( f"added {cards_list[idx]} of  key{key} at {idx} " ) 
				else:
					cards_map[key].append(idx) # since there are duplicates

	print("Cards map after taking photo: ",cards_map)
@delay		
def find_SetsH():

	for i in range(blank_button_idx-1): # All pair combinations
		for j in range(i+1,blank_button_idx):
			
			# to check which ones are being compared
			# print("T", (i,j) , end=' ')

			# Get the 3rd member of the set
			if cards_list[i] and cards_list[j] and cards_list[i] != cards_list[j]: # don't select yourself/and Nones
				
				matchingpiece = (SetCard.getMatch(cards_list[i],cards_list[j]))
				key = matchingpiece.hash()
				
				if key in cards_map: # look for 3rd member of set
					
					
					# obtain the hash values for each card
					complete_set = cards_list[i].hash(), cards_list[j].hash(), key

					print(f"Found this set: {cards_list[i]}, {cards_list[j]}, {matchingpiece}")
					
					click_Sets(i, j, cards_map[key][-1])
					time.sleep(1.1)
					driver.implicitly_wait(2)

					for k in complete_set:
					
						card_indices = cards_map[k] # Retrieve the indices of every card with that hash
						index = card_indices.pop()
						
						print(f"Removing index {index} from the card list")
						cards_list[index] = None # Remove from list

						if len(cards_map[k]) == 0: # We emptied out the list, remove that hash entry
							print("cleared the set list")
							cards_map.pop(k, None)						 


					# Remove from set
						print("Now cards list looks like this: ", cards_list)
						print("map contains now", cards_map)
"""		