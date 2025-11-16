# Weather Outfit App - Feature Testing Guide

## 🎯 How to Test the Location-Aware Features

The quick action buttons and outfit suggestions change based on **which city you search for**. Here's what to test:

---

## ✅ TEST 1: Seattle (Hiking/Rain)

**What to do:**
1. Type "Seattle" in the search box
2. Press Enter or click the heart icon

**What you should see:**
- Quick action buttons change to:
  - "Good for hiking?"
    - "Camping tonight?"
      - "Rain gear needed?"
      - Weather icon updates to match Seattle's weather
      - Outfit suggestions include jackets for cooler weather

      ---

      ## ✅ TEST 2: Denver (Snow/Mountains)

      **What to do:**
      1. Type "Denver" in the search box
      2. Press Enter

      **What you should see:**
      - Quick action buttons change to:
        - "Mountain hiking?"
          - "Cold weather gear?"
            - "What if it snows?"
            - Outfit suggestions include warm layers

            ---

            ## ✅ TEST 3: Miami (Beach/Hot)

            **What to do:**
            1. Type "Miami" in the search box
            2. Press Enter

            **What you should see:**
            - Quick action buttons change to:
              - "Beach ready?"
                - "Pool party?"
                  - "Outdoor activities?"
                  - Outfit suggestions lighter clothing
                  - May include sunglasses if sunny

                  ---

                  ## ✅ TEST 4: New York (City)

                  **What to do:**
                  1. Type "New York" in the search box
                  2. Press Enter

                  **What you should see:**
                  - Quick action buttons change to:
                    - "City walking?"
                      - "Any formal options?"
                        - "What about layering?"

                        ---

                        ## 🎨 Weather Icon Colors

                        The weather icon (top of weather card) changes color based on conditions:

                        - ☀️ **Clear/Sunny** → Yellow/Amber icon
                        - 🌧️ **Rainy** → Blue icon
                        - ❄️ **Snowy** → Cyan/Light blue icon
                        - ☁️ **Cloudy** → Gray icon
                        - ⛈️ **Stormy** → Purple icon

                        **Note:** Most cities currently show "partly cloudy" from the weather API.

                        ---

                        ## 👕 Outfit Icons

                        Each outfit item has a specific icon:
                        - T-Shirt → Shirt icon
                        - Jeans → Apparel icon
                        - Sneakers → Soccer ball icon
                        - **Watch/Bracelet** → Watch icon ⌚
                        - **Backpack/Bag** → Shopping bag icon 🛍️
                        - **Belt** → Fitness/dumbbell icon 💪
                        - **Socks** → Stockings icon (when shown)
                        - **Scarf** → Scatter plot icon (when shown in cold weather)
                        - **Winter Hat** → Safety helmet icon (when shown)

                        ---

                        ## 🧊 To See Cold Weather Items (Socks, Scarf, Winter Hat):

                        Search for a **very cold city** or wait for colder weather. The items appear based on temperature:

                        - **Scarf** → Shows when temp < 50°F
                        - **Winter Hat** → Shows when temp < 45°F
                        - **Gloves** → Shows when temp < 35°F
                        - **Socks** → Shows in most outfits (6-8 items total)

                        **Try:** Search for "Fairbanks Alaska" or "Minneapolis" in winter

                        ---

                        ## 🔔 Testing Notifications & Settings

                        1. **Click the bell icon** (🔔) → Opens notifications page with weather alerts
                        2. **Click the gear icon** (⚙️) → Opens settings page with all preferences

                        ---

                        ## ❓ If Features Still Don't Work:

                        1. **Hard refresh** your browser: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
                        2. **Check browser console** for errors (F12 → Console tab)
                        3. **Try different cities** from the lists above

                        ---

                        ## 📊 Current Status

                        ✅ Weather icon updates dynamically
                        ✅ Quick actions change based on city
                        ✅ Outfit items have correct icons
                        ✅ Notifications & Settings work
                        ✅ 6-8 outfit items generated

                        The features are **working** - you just need to search for different cities to see them activate!
                        