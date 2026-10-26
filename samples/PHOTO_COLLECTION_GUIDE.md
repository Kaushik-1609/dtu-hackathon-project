# DoubtLens — Test Photo Collection Guide & Benchmark Outputs

This document defines the 6 benchmark multimodal test photos for [`samples/`](./) used to demonstrate and evaluate DoubtLens at **Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)**.

---

## 📸 Benchmark Test Photos & Expected Outputs

### 1. `samples/physics_newton_law.jpg` (Textbook Page — Mechanics & Vectors)
* **What to Capture:** A printed textbook page with a diagram showing a $5\text{ kg}$ block on a rough horizontal surface, pulled right with $F = 20\text{ N}$, friction force $f_k = 5\text{ N}$, asking for acceleration.
* **Why it Tests Gemma 4:** Tests combined image comprehension: reading printed problem typography + resolving physical force vector arrows.
* **What Good Output Looks Like:**
  * **`topic`**: *"Newton's Second Law of Motion"*
  * **`explanation`**: *"When multiple forces act on a body, the net unbalanced force produces an acceleration proportional to the net force and inversely proportional to the mass ($F_{\text{net}} = m \cdot a$)."*
  * **`steps`**:
    1. Identify given values: Pull force $F = 20\text{ N}$, Friction $f_k = 5\text{ N}$, Mass $m = 5\text{ kg}$.
    2. Calculate net horizontal force: $F_{\text{net}} = F - f_k = 20\text{ N} - 5\text{ N} = 15\text{ N}$ to the right.
    3. Apply Newton's Second Law: $a = \frac{F_{\text{net}}}{m} = \frac{15\text{ N}}{5\text{ kg}}$.
    4. Calculate final acceleration: $a = 3\text{ m/s}^2$ directed to the right.
  * **`key_points`**:
    * Always sum collinear forces algebraically before dividing by mass.
    * Do not forget friction opposes the direction of applied motion.
    * Acceleration unit is $\text{m/s}^2$, not $\text{N}$ or $\text{m/s}$.

---

### 2. `samples/circuit_resistors.jpg` (Electrical Schematic — Circuits)
* **What to Capture:** A clear electrical schematic diagram showing a $12\text{V}$ battery connected to a parallel branch of $6\,\Omega$ and $3\,\Omega$ in series with a $4\,\Omega$ resistor.
* **Why it Tests Gemma 4:** Tests pure diagram/schematic recognition without inline explanatory sentences; model must identify node connectivity.
* **What Good Output Looks Like:**
  * **`topic`**: *"Equivalent Resistance in Series-Parallel DC Circuits"*
  * **`explanation`**: *"To find the total current flowing from the battery, reduce parallel resistor combinations into single equivalent values, then sum remaining series resistances."*
  * **`steps`**:
    1. Identify parallel branch: $R_1 = 6\,\Omega$ in parallel with $R_2 = 3\,\Omega$.
    2. Compute parallel equivalent: $R_p = \frac{R_1 \cdot R_2}{R_1 + R_2} = \frac{18}{9} = 2\,\Omega$.
    3. Add series resistor: $R_{\text{total}} = R_p + R_3 = 2\,\Omega + 4\,\Omega = 6\,\Omega$.
    4. Apply Ohm's Law for circuit current: $I = \frac{V}{R_{\text{total}}} = \frac{12\text{V}}{6\,\Omega} = 2\text{ A}$.
  * **`key_points`**:
    * Parallel branches share identical voltage; series branches share identical current.
    * Equivalent resistance of parallel resistors is always smaller than the smallest branch resistor.
    * Total circuit current depends on total equivalent resistance.

---

### 3. `samples/handwritten_calculus.jpg` (Messy Notebook — Calculus)
* **What to Capture:** A photo of a student's ruled paper notebook with a handwritten integration problem: $\int x e^{2x} \, dx$ with an incomplete integration-by-parts attempt.
* **Why it Tests Gemma 4:** Tests messy student handwriting, superscript/subscript detection, mathematical symbol recognition ($\int, dx, e^{2x}$), and spotting student stumbling blocks.
* **What Good Output Looks Like:**
  * **`topic`**: *"Integration by Parts (LIATE Rule)"*
  * **`explanation`**: *"When integrating the product of an algebraic term and an exponential term, use Integration by Parts: $\int u \, dv = u \cdot v - \int v \, du$."*
  * **`steps`**:
    1. Select $u$ and $dv$ using LIATE: Let $u = x$ (algebraic) and $dv = e^{2x} \, dx$ (exponential).
    2. Compute derivatives and integrals: $du = dx$ and $v = \frac{1}{2} e^{2x}$.
    3. Substitute into formula: $\int x e^{2x} \, dx = x \left(\frac{1}{2} e^{2x}\right) - \int \frac{1}{2} e^{2x} \, dx$.
    4. Evaluate remaining integral and add constant: $\frac{1}{2} x e^{2x} - \frac{1}{4} e^{2x} + C$.
  * **`key_points`**:
    * Remember dividing by 2 when integrating $e^{2x}$.
    * Factor out common term $\frac{1}{4} e^{2x}(2x - 1) + C$ for clean algebraic form.
    * Never forget the arbitrary constant of integration $+ C$.

---

### 4. `samples/chemistry_organic_reaction.jpg` (Chemical Structures & Mechanisms)
* **What to Capture:** A printed or drawn reaction mechanism showing 2-bromopropane reacting with aqueous $\text{KOH}$ with curved electron arrows showing nucleophilic substitution.
* **Why it Tests Gemma 4:** Tests structural organic chemical formulas, functional groups, bond angles, and arrow-pushing mechanisms.
* **What Good Output Looks Like:**
  * **`topic`**: *"Nucleophilic Substitution ($S_N2$ vs $S_N1$) of Alkyl Halides"*
  * **`explanation`**: *"Hydroxide ion acts as a strong nucleophile, replacing the bromide leaving group on the secondary alkyl halide to synthesize propan-2-ol."*
  * **`steps`**:
    1. Identify substrate and reagent: 2-bromopropane (secondary alkyl halide) and $\text{OH}^-$ nucleophile.
    2. Analyze mechanism pathway: Secondary carbocation allows both $S_N1$ and $S_N2$; in polar protic solvent, carbocation intermediate forms.
    3. Leaving group departure: Bromide ($\text{Br}^-$) departs, leaving a planar carbocation.
    4. Nucleophilic attack: $\text{OH}^-$ attacks planar center to yield propan-2-ol with inorganic byproduct $\text{KBr}$.
  * **`key_points`**:
    * Good leaving group ability correlates with conjugate base stability ($\text{Br}^-$ is stable).
    * Aqueous $\text{KOH}$ favors substitution (alcohol); alcoholic $\text{KOH}$ favors elimination (alkene).
    * Stereochemical outcome depends on backside attack versus planar carbocation.

---

### 5. `samples/geometry_circle_theorems.jpg` (Geometric Proofs & Diagrams)
* **What to Capture:** A circle with center $O$, an arc subtending angle $\angle AOB$ at the center and $\angle ACB$ on the circumference, with inscribed angle values given.
* **Why it Tests Gemma 4:** Tests spatial reasoning, geometric label parsing ($A, B, C, O$), and angle deduction.
* **What Good Output Looks Like:**
  * **`topic`**: *"Inscribed Angle Theorem on Circles"*
  * **`explanation`**: *"The angle subtended by an arc at the center of a circle is double the angle subtended by it at any point on the remaining part of the circle."*
  * **`steps`**:
    1. Identify given geometry: Arc $AB$ subtends central angle $\angle AOB = 80^\circ$.
    2. Locate inscribed angle: Point $C$ lies on major arc circumference subtending $\angle ACB$.
    3. Apply Inscribed Angle Theorem: $\angle ACB = \frac{1}{2} \angle AOB$.
    4. Compute angle: $\angle ACB = \frac{1}{2} \times 80^\circ = 40^\circ$.
  * **`key_points`**:
    * Both angles must share the exact same intercepted arc.
    * An angle inscribed in a semicircle is always a right angle ($90^\circ$).
    * Opposite angles of a cyclic quadrilateral sum to $180^\circ$.

---

### 6. `samples/hindi_textbook_kinematics.jpg` (NCERT Hindi Medium Textbook)
* **What to Capture:** A printed Hindi NCERT Physics textbook snippet: *"एक पिंड विरामावस्था से $2\text{ m/s}^2$ के एकसमान त्वरण से चलना प्रारंभ करता है। $5$ सेकंड बाद इसका वेग तथा तय की गई दूरी ज्ञात कीजिए।"*
* **Why it Tests Gemma 4:** Tests native Hindi OCR, Devanagari numerals/scientific vocabulary, and end-to-end Devanagari mathematical resolution.
* **What Good Output Looks Like:**
  * **`topic`**: *"एकसमान त्वरित गति के समीकरण (Kinematics Equations of Motion)"*
  * **`explanation`**: *"जब कोई वस्तु एकसमान त्वरण से चलती है, तो उसके वेग, त्वरण, समय और विस्थापन के बीच संबंध को गति के तीन समीकरणों द्वारा हल किया जाता है।"*
  * **`steps`**:
    1. दिए गए मान पहचानें: प्रारंभिक वेग $u = 0\text{ m/s}$ (विरामावस्था), त्वरण $a = 2\text{ m/s}^2$, समय $t = 5\text{ s}$।
    2. अंतिम वेग ज्ञात करने के लिए प्रथम समीकरण लागू करें: $v = u + at = 0 + (2 \times 5) = 10\text{ m/s}$।
    3. तय की गई दूरी के लिए द्वितीय समीकरण लागू करें: $s = ut + \frac{1}{2}at^2$।
    4. गणना करें: $s = 0 \times 5 + \frac{1}{2}(2)(5)^2 = 25\text{ मीटर}$।
  * **`key_points`**:
    * 'विरामावस्था' (Rest) का अर्थ प्रारंभिक वेग $u = 0$ होता है।
    * गति के समीकरण केवल तभी मान्य होते हैं जब त्वरण 'एकसमान' (Constant) हो।
    * विस्थापन की मानक इकाई मीटर ($\text{m}$) और वेग की $\text{m/s}$ होती है।
