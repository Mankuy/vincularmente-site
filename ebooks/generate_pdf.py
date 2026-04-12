#!/usr/bin/env python3
"""Generate PDF for 'Amás como amás' ebook."""

from fpdf import FPDF
import os

FONT_REG = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_ITAL = '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf'

class EbookPDF(FPDF):
    ACCENT = (147, 51, 234)  # purple
    ACCENT2 = (233, 69, 96)  # pink/red
    
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Sans', '', 7)
        self.set_text_color(170, 170, 170)
        self.cell(0, 5, 'vincularmente', align='R')
        self.ln(3)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(5)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('Sans', 'I', 7)
        self.set_text_color(170, 170, 170)
        self.cell(0, 10, f'{self.page_no()}', align='C')

    def cover_page(self):
        self.set_y(60)
        # Decorative line
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.5)
        self.line(self.w/2 - 25, self.get_y(), self.w/2 + 25, self.get_y())
        self.ln(12)
        # Title
        self.set_font('Sans', 'B', 32)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 16, 'Amás como amás', align='C')
        self.ln(20)
        # Subtitle
        self.set_font('Sans', '', 14)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, 'Estilos de apego y por qué elegís\nsiempre al mismo tipo de persona', align='C')
        self.ln(25)
        # Brand
        self.set_font('Sans', 'I', 12)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, 'vincularmente', align='C')
        self.ln(6)
        self.set_font('Sans', '', 9)
        self.set_text_color(170, 170, 170)
        self.cell(0, 6, 'Salud mental, vínculos y realidad.', align='C')
        self.add_page()

    def section_title(self, text):
        self.set_font('Sans', 'B', 16)
        self.set_text_color(*self.ACCENT)
        self.ln(4)
        self.cell(0, 10, text)
        self.ln(12)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, text):
        self.set_font('Sans', 'B', 12)
        self.set_text_color(60, 60, 60)
        self.ln(2)
        self.cell(0, 8, text)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def body_text(self, txt, size=10):
        if self.get_y() > self.h - 25:
            self.add_page()
        self.set_font('Sans', '', size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, txt)
        self.ln(3)

    def bold_text(self, txt, size=10):
        if self.get_y() > self.h - 25:
            self.add_page()
        self.set_font('Sans', 'B', size)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, txt)
        self.ln(3)

    def bullet(self, txt):
        if self.get_y() > self.h - 20:
            self.add_page()
        self.set_font('Sans', '', 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(6, 6, chr(8226))
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 6, txt)
        self.ln(2)

    def example_block(self, txt):
        if self.get_y() > self.h - 30:
            self.add_page()
        self.set_font('Sans', 'I', 9.5)
        self.set_text_color(100, 100, 100)
        self.set_fill_color(248, 245, 255)
        x = self.get_x()
        self.set_x(self.l_margin + 5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 10, 5.5, txt, fill=True)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def divider(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(self.w/2 - 15, self.get_y(), self.w/2 + 15, self.get_y())
        self.ln(6)

    def cta_box(self, txt):
        if self.get_y() > self.h - 40:
            self.add_page()
        self.ln(4)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.5)
        y0 = self.get_y()
        self.set_x(self.l_margin + 10)
        self.set_font('Sans', 'B', 11)
        self.set_text_color(*self.ACCENT)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 20, 7, txt, align='C')
        y1 = self.get_y()
        self.rect(self.l_margin + 10, y0 - 2, self.w - self.l_margin - self.r_margin - 20, y1 - y0 + 4)
        self.ln(6)
        self.set_text_color(0, 0, 0)

# --- Build PDF ---
pdf = EbookPDF()
pdf.add_font('Sans', '', FONT_REG)
pdf.add_font('Sans', 'B', FONT_BOLD)
pdf.add_font('Sans', 'I', FONT_ITAL)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Cover
pdf.cover_page()

# Cap 1
pdf.section_title('Capítulo 1: ¿Por qué repito siempre lo mismo?')
pdf.body_text('Te juro que esta vez iba a ser distinto.')
pdf.body_text('Conocés a alguien. Sentís mariposas. Pensás "este/a es diferente". Sentís que fluye, que todo es intenso, que todo es perfecto.')
pdf.body_text('Y después, de a poquito o de golpe, todo se repite.')
pdf.body_text('O se pone distante. O te volvés loco/a por la otra persona. O aparecen los mismos conflictos, las mismas peleas, las mismas frases.')
pdf.bold_text('"Siempre me pasa lo mismo."')
pdf.body_text('Y tenés razón. Siempre te pasa lo mismo. Pero no porque tengas mala suerte, o porque "todas/os son iguales", o porque "no te merecés algo mejor".')
pdf.body_text('Te pasa lo mismo porque elegís con el mismo sistema cada vez.')
pdf.body_text('Ese sistema tiene un nombre: tu estilo de apego.')
pdf.body_text('Y hasta que no lo entiendas, vas a seguir tropezando con la misma piedra.')

# Cap 2
pdf.section_title('Capítulo 2: ¿Qué es el apego y cómo se forma?')
pdf.body_text('El apego es la forma en que aprendiste a vincularte con otra persona.')
pdf.body_text('No lo elegiste. Se formó antes de que tuvieras memoria consciente, entre los 0 y los 5 años, mirando cómo te cuidaban tus viejos o quien te cuidó.')
pdf.body_text('¿Tu mamá o tu papá te atendían cuando llorabas? ¿Te dejaban explorar y volvías seguro/a? ¿O a veces estaban y a veces no? ¿O nunca estaban?')
pdf.body_text('Cada una de esas respuestas te enseñó algo:')
pdf.example_block('"Si lloro, alguien viene." → Las personas son seguras.\n"A veces vienen y a veces no." → No puedo confiar del todo.\n"Si lloro, nadie viene." → Tengo que arreglarme solo/a.')
pdf.body_text('Esas creencias quedaron grabadas en vos. No como pensamientos, sino como respuestas automáticas.')
pdf.body_text('Por eso a veces "sabés" que algo no te hace bien, pero no podés dejar de hacerlo. No es que sos débil. Es que tu sistema nervioso está actuando con un programa que se instaló hace 20 o 30 años.')
pdf.bold_text('La buena noticia: se puede actualizar.')

# Cap 3
pdf.section_title('Capítulo 3: Los 4 estilos de apego')
pdf.body_text('Hay 4 estilos principales. La mayoría de la gente tiene uno dominante, a veces mezclado con otro.')

pdf.subsection_title('3.1 Apego seguro')
pdf.body_text('La persona con apego seguro:')
pdf.bullet('Confía en que la otra persona va a estar.')
pdf.bullet('Puede estar cerca sin angustiarse.')
pdf.bullet('Puede estar lejos sin entrar en pánico.')
pdf.bullet('Comunica lo que necesita sin dramatismo.')
pdf.bullet('Tolera los conflictos sin sentir que todo se termina.')
pdf.body_text('¿Cómo se forma? Cuidadores que estuvieron disponibles de forma consistente. No perfectos, sino predecibles.')
pdf.example_block('Ejemplo: "Me peleé con mi pareja. Me duele, pero sé que lo vamos a hablar. No pienso que me va a dejar."')
pdf.body_text('Lo que diferencia al apego seguro del inseguro: no pensás "¿y si me abandona?"')
pdf.body_text('La realidad: aproximadamente el 50-60% de la población tiene apego seguro. El resto tiene algún estilo inseguro.')

pdf.divider()

pdf.subsection_title('3.2 Apego ansioso (o "preocupado")')
pdf.body_text('La persona con apego ansioso:')
pdf.bullet('Necesita confirmación constante de que la otra persona lo/la quiere.')
pdf.bullet('Se angustia cuando no responden rápido.')
pdf.bullet('Tiende a idealizar a la otra persona.')
pdf.bullet('Siente que quiere más de lo que la otra persona puede dar.')
pdf.bullet('Cuando hay distancia, interpreta lo peor.')
pdf.body_text('¿Cómo se forma? Cuidadores que a veces estaban y a veces no. El niño/a nunca supo qué esperar, así que aprendió a "vigilar" constantemente.')
pdf.example_block('Ejemplo: "Me mandó un audio hace 3 horas y no me contestó. Seguro está con otra persona. O ya se aburrió de mí. ¿Le mando otro mensaje? No, mejor espero. Pero no puedo esperar."')
pdf.body_text('La persona ansiosa no es "intensa" por gusto. Su sistema de alarma interno está activado todo el tiempo.')

pdf.divider()

pdf.subsection_title('3.3 Apego evitativo (o "distante")')
pdf.body_text('La persona con apego evitativo:')
pdf.bullet('Valora mucho su independencia.')
pdf.bullet('Se incomoda cuando la otra persona se pone "demasiado" cercana.')
pdf.bullet('Tiende a mantener distancia emocional.')
pdf.bullet('Cuando las cosas se ponen serias, se aleja o busca defectos en el otro/a.')
pdf.bullet('Prefiere resolver solo/a antes que pedir ayuda.')
pdf.body_text('¿Cómo se forma? Cuidadores que estaban presentes físicamente pero ausentes emocionalmente, o que castigaban al niño/a por mostrar necesidades.')
pdf.example_block('Ejemplo: "Todo iba bien, pero últimamente me pide que le cuente más cosas, que pase más tiempo juntos, que le diga qué siento. Siento que me asfixia. Necesito espacio."')
pdf.body_text('La persona evitativa no es "fría" por gusto. Aprendió que mostrar necesidades es peligroso. Su distancia es protección.')

pdf.divider()

pdf.subsection_title('3.4 Apego desorganizado (o "ansioso-evitativo")')
pdf.body_text('La persona con apego desorganizado:')
pdf.bullet('Quiere estar cerca pero le da miedo.')
pdf.bullet('Alterna entre acercarse y alejarse.')
pdf.bullet('Tiene relaciones muy intensas y caóticas.')
pdf.bullet('No sabe qué quiere: un día idealiza, al otro día quiere huir.')
pdf.bullet('A veces sabotea relaciones que le hacen bien.')
pdf.body_text('¿Cómo se forma? Cuidadores que eran fuente de miedo y seguridad al mismo tiempo (abuso, negligencia severa, adicciones, violencia doméstica).')
pdf.example_block('Ejemplo: "Lo extraño cuando no está. Pero cuando está, quiero que se vaya. No entiendo qué me pasa."')
pdf.body_text('Este es el estilo más complejo y el que más sufrimiento genera, porque no hay una "receta" clara para vincularse.')

# Cap 4
pdf.section_title('Capítulo 4: Identificá tu estilo')
pdf.body_text('No necesitás un test profesional para tener una idea general de tu estilo. Respondé estas preguntas con honestidad:')

pdf.bold_text('1. Cuando tu pareja no te contesta el celular, ¿qué pensás primero?')
pdf.bullet('a) "Estará ocupado/a." (seguro)')
pdf.bullet('b) "¿Y si ya no le intereso?" (ansioso)')
pdf.bullet('c) "Mejor, así tengo mi espacio." (evitativo)')
pdf.bullet('d) No sé, depende del día. (desorganizado)')
pdf.ln(2)

pdf.bold_text('2. Cuando alguien se acerca mucho emocionalmente, ¿qué sentís?')
pdf.bullet('a) Me gusta. (seguro)')
pdf.bullet('b) Me encanta pero tengo miedo de perderlo. (ansioso)')
pdf.bullet('c) Me incomoda. Necesito espacio. (evitativo)')
pdf.bullet('d) Quiero que se acerque y a la vez quiero huir. (desorganizado)')
pdf.ln(2)

pdf.bold_text('3. Después de una pelea, ¿qué hacés?')
pdf.bullet('a) Me calmo y lo hablo. (seguro)')
pdf.bullet('b) Necesito resolverlo YA. No puedo esperar. (ansioso)')
pdf.bullet('c) Necesito tiempo solo/a. Después vemos. (evitativo)')
pdf.bullet('d) Depende. A veces suplico, a veces desaparezco. (desorganizado)')
pdf.ln(2)

pdf.bold_text('4. ¿Cómo elegís a tus parejas?')
pdf.bullet('a) Busco alguien que me sume. (seguro)')
pdf.bullet('b) Me atrae quien me hace sentir intenso/a. (ansioso)')
pdf.bullet('c) Me atrae quien no me exige demasiado. (evitativo)')
pdf.bullet('d) Me atrae quien me desestabiliza. (desorganizado)')
pdf.ln(3)

pdf.body_text('No hay respuestas correctas ni incorrectas. Lo importante es que reconozcas el patrón.')
pdf.body_text('Y si te identificaste con más de uno: es normal. Los estilos no son cajas cerradas. Son tendencias.')

# Cap 5
pdf.section_title('Capítulo 5: Por qué lo ansioso y lo evitativo se atraen')
pdf.body_text('Acá viene lo que nadie te explicó.')
pdf.body_text('Si sos ansioso/a, ¿con quién salís siempre? Con alguien evitativo.')
pdf.body_text('Y si sos evitativo/a, ¿quién te persigue? Alguien ansioso.')
pdf.body_text('No es casualidad. Es un imán.')
pdf.body_text('La persona ansiosa necesita cercanía. La persona evitativa necesita distancia.')
pdf.bold_text('Cuando se encuentran:')
pdf.bullet('El ansioso se acerca.')
pdf.bullet('El evitativo se aleja.')
pdf.bullet('El ansioso entra en pánico y se acerca más.')
pdf.bullet('El evitativo se siente asfixiado y se aleja más.')
pdf.body_text('Y así en bucle.')
pdf.body_text('Y lo peor: eso que ambos sienten les parece "amor". La intensidad, la angustia, la incertidumbre. "Si siento tanto, es porque lo amo."')
pdf.bold_text('No. Lo que sentís es tu sistema de alarma disparado.')
pdf.body_text('El amor real se siente... tranquilo. Como llegar a casa después de un día largo. Y eso es lo más aterrador de todo para alguien con apego inseguro, porque su cerebro no lo reconoce como amor. Lo confunde con aburrimiento.')
pdf.example_block('"Con este/a no siento nada."\nClaro. Porque no hay drama. Y sin drama, tu sistema no sabe qué hacer.')

# Cap 6
pdf.section_title('Capítulo 6: Cómo cambiar tu estilo de apego')
pdf.body_text('Tu estilo de apego no es una condena. No es "soy ansioso/a y listo, así voy a ser siempre".')
pdf.bold_text('Se puede cambiar. Pero no con afirmaciones frente al espejo. Se cambia con experiencias nuevas.')
pdf.body_text('No es que tengas que "arreglarte". Es que tu sistema nervioso aprendió una forma de estar en relación, y ahora puede aprender una nueva. La diferencia: con consciencia y acompañamiento.')

pdf.subsection_title('Si sos ansioso/a:')
pdf.bullet('Antes de mandar el tercer mensaje, preguntate: "¿Estoy reaccionando a lo que pasa o a lo que imagino?"')
pdf.bullet('Buscá ocupar tu tiempo con cosas que sean tuyas. Tu ansiedad baja cuando tu vida no gira alrededor de la otra persona.')
pdf.bullet('Aprendé a tolerar la incertidumbre. No necesitás saber "qué somos" a los dos meses.')
pdf.bullet('Terapia. En serio. Un buen terapeuta te va a dar lo que tu cuidador no pudo: consistencia.')

pdf.subsection_title('Si sos evitativo/a:')
pdf.bullet('Cuando sientas ganas de alejarte, preguntate: "¿Me estoy alejando porque esto no me sirve o porque me da miedo?"')
pdf.bullet('Practicá quedarte un poquito más de lo que te sale cómodo.')
pdf.bullet('Aprendé a pedir ayuda. Empezá por cosas pequeñas.')
pdf.bullet('Terapia. Tu distancia te protegió de chico/a, pero ahora te está aislando.')

pdf.subsection_title('Si sos desorganizado/a:')
pdf.bullet('No es "tu culpa". Lo que te pasó de chico/a no fue tu responsabilidad.')
pdf.bullet('Buscá un terapeuta especializado en trauma. No cualquier terapeuta.')
pdf.bullet('No entres en una relación hasta que tengas herramientas. No por castigo, sino porque sin herramientas vas a repetir.')
pdf.bullet('La curación es posible, pero lleva tiempo y acompañamiento profesional.')

# Cap 7
pdf.section_title('Capítulo 7: Cómo elegir mejor la próxima vez')
pdf.body_text('El cambio no es solo entender tu estilo. Es aprender a elegir distinto.')

pdf.bold_text('Regla 1: Si te da mucha mariposa, desconfiá.')
pdf.body_text('El "fuego" que sentís al principio muchas veces es tu sistema de apego reconociendo un patrón conocido. Lo conocido no siempre es lo mejor.')

pdf.bold_text('Regla 2: Buscá consistencia, no intensidad.')
pdf.body_text('¿La otra persona hace lo que dice? ¿Está presente sin que se lo pidas? ¿Te contesta sin que tengas que suplicar? Eso vale más que mil poemas.')

pdf.bold_text('Regla 3: Date tiempo.')
pdf.body_text('No decidas si alguien es "para vos" en la primera semana. Los estilos inseguros se disfrazan bien al principio. Dales tiempo a que salgan.')

pdf.bold_text('Regla 4: Preguntate "¿me siento seguro/a o me siento emocionado/a?"')
pdf.body_text('Seguro y emocionado no son lo mismo. El amor sano se siente como llegar a casa, no como un tobogán.')

pdf.bold_text('Regla 5: Si ya estás en una relación y ambos tienen apego inseguro, hay esperanza.')
pdf.body_text('Pero necesitan los dos estar dispuestos a verse, a entenderse, a cambiar. Si solo uno hace el trabajo, no funciona.')

# Cierre
pdf.section_title('Cerrando')
pdf.body_text('Tu estilo de apego no te define. Te describe.')
pdf.body_text('No sos "el ansioso" ni "la evitativa". Sos una persona que aprendió a protegerse de una forma específica cuando era chico/a.')
pdf.body_text('Y ahora, como adulto/a, podés elegir si querés seguir usando esa estrategia o querés aprender una nueva.')
pdf.body_text('No es fácil. No es rápido. Pero es posible.')
pdf.body_text('Y el primer paso es este: darte cuenta de que el patrón existe.')
pdf.bold_text('Ya lo hiciste.')
pdf.body_text('Ahora falta lo demás, y eso lo podés hacer con acompañamiento.')
pdf.body_text('Si querés que te ayude a entender tu caso puntual, escribime.')
pdf.bold_text('Estoy acá.')

# CTA
pdf.divider()
pdf.body_text('Este ebook es el primer paso. El siguiente es el acompañamiento.', size=10)
pdf.ln(2)
pdf.bold_text('¿Querés profundizar?', size=11)
pdf.body_text('"No estás Rot@" - Mi primer ebook sobre relaciones tóxicas')
pdf.body_text('go.hotmart.com/Q105244008P ($4.99)')
pdf.ln(2)
pdf.bold_text('¿Querés una sesión?', size=11)
pdf.body_text('Escribime. Trabajamos tu caso específico.')
pdf.body_text('WhatsApp: 598 991 48 716')
pdf.ln(2)
pdf.bold_text('Estoy acá.', size=11)

# Final
pdf.ln(10)
pdf.set_font('Sans', 'B', 14)
pdf.set_text_color(*pdf.ACCENT)
pdf.cell(0, 8, 'vincularmente', align='C')
pdf.ln(6)
pdf.set_font('Sans', '', 9)
pdf.set_text_color(130, 130, 130)
pdf.cell(0, 6, 'Salud mental, vínculos y realidad.', align='C')
pdf.ln(10)
pdf.set_font('Sans', '', 7)
pdf.set_text_color(170, 170, 170)
pdf.cell(0, 6, '© 2025 vincularmente. Todos los derechos reservados.', align='C')

# Save
out = '/home/facajgs/vincularmente-site/ebooks/amas-como-amas.pdf'
pdf.output(out)
print(f'PDF generado: {out}')
print(f'Páginas: {pdf.pages_count}')
