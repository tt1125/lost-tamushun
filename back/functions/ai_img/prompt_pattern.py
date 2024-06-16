def convert_to_prompt(keyword):
        if keyword == "harry_potter":
            return """ A magnificent photo that looks like a scene from the Harry Potter world, 
            featuring magical landscapes, enchanting castles, and mystical creatures.,photorealistic , 4K resolution,
            High resolution, masterpiece, realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "disney":
            return """A magical photo that looks like a scene from a Disney movie, featuring enchanting castles, 
            beautiful princesses, and adorable animals.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "gundam":
            return """A futuristic photo that looks like a scene from a Gundam anime, featuring giant robots, 
            advanced technology, and epic battles.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "pokemon":
            return """A cute photo that looks like a scene from a Pokemon game, featuring adorable creatures, 
            magical landscapes, and exciting adventures.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "star_wars":
            return """An epic photo that looks like a scene from a Star Wars movie, featuring futuristic cities, 
            space battles, and alien creatures.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "marvel":
            return """A thrilling photo that looks like a scene from a Marvel movie, featuring superheroes, 
            epic battles, and amazing powers.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        elif keyword == "egipt":
            return """A mysterious photo that looks like a scene from ancient Egypt, featuring pyramids, 
            pharaohs, and hieroglyphics.,photorealistic , 4K resolution, High resolution, masterpiece, 
            realistic, highly detailed, cinematic lighting, vibrant colors."""
        
        else:
             ""

if __name__ == "__main__":
    print(convert_to_prompt("harry_potter"))