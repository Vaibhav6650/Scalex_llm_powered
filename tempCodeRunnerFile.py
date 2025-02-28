query = f"""Generate a concise and professional opening line for a cold email.

    ### Objective:
    I run an agency named ScaleX, where we provide digital services to businesses. I send cold emails based on Instagram profiles. The email follows a general template, but I want to personalize the opening with a **structured and specific** compliment that makes it feel like I have analyzed their brand.

    ### Format Requirement:
    - The sentence **must** start with **'Your [business/brand]...'**
    - It **must** follow this format:
      **'Your [expertise/focus] in [industry/niche], along with your [unique element], establishes/highlights/positions your brand as [value proposition].'**

    ### Guidelines:
    - **Keep it factual**—do not add information that is not explicitly in the provided bio.
    - **Do not be vague**—avoid words like 'high-quality' or 'unique' without explaining why.
    - **Focus on tangible aspects** like:
      - Industry expertise
      - Specialized offerings
      - Target audience impact
    - **Maintain the structured format.**

    ### Example Bio:
    'Mumbai’s First Korean Bistro & Specialty Coffee Destination. Brewing a leisurely and comforting experience for you every time.'

    ### Expected Output:
    'Your focus on Korean cuisine and specialty coffee, combined with your commitment to creating a comforting atmosphere, establishes your café as a go-to destination for food lovers in Mumbai.'

    Now, generate a structured, concise, and accurate personalized compliment for this bio:
    """