from manim import *

class CPPOnlineValueChain(Scene):
    def construct(self):
        # Define participants with distinct colors
        ux = Text("UX", color=BLUE, font_size=36).to_edge(LEFT)
        domain_api = Text("Domain API Layer", color=GREEN, font_size=36).to_edge(UP)
        microvalidator = Text("MicroValidator API", color=YELLOW, font_size=36).to_edge(RIGHT)
        ftm = Text("FTM", color=RED, font_size=36).to_edge(DOWN)

        # Display participants
        self.play(FadeIn(ux), FadeIn(domain_api), FadeIn(microvalidator), FadeIn(ftm))
        self.wait(1)

        # Draw lifelines for participants
        ux_line = Line(ux.get_bottom(), ux.get_bottom() + DOWN * 5, color=BLUE)
        domain_api_line = Line(domain_api.get_bottom(), domain_api.get_bottom() + DOWN * 5, color=GREEN)
        microvalidator_line = Line(microvalidator.get_bottom(), microvalidator.get_bottom() + DOWN * 5, color=YELLOW)
        ftm_line = Line(ftm.get_top(), ftm.get_top() + UP * 5, color=RED)

        self.play(Create(ux_line), Create(domain_api_line), Create(microvalidator_line), Create(ftm_line))
        self.wait(1)

        # Helper function to create sequence step
        def sequence_step(start_obj, end_obj, text, color):
            arrow = Arrow(
                start=start_obj.get_center(),
                end=end_obj.get_center(),
                buff=0.5,
                color=color,
                stroke_width=3
            )
            # Reduced font size by 30% and added glow
            label = Text(text, font_size=16, color=color).move_to((start_obj.get_center() + end_obj.get_center()) / 2 + UP)
            glow_label = label.copy().set_opacity(0.3).set_color(WHITE)

            glow_arrow = arrow.copy().set_stroke(width=10, opacity=0.3).set_color(YELLOW)

            # Show glow, arrow, and text
            self.play(FadeIn(glow_label), Create(glow_arrow), Create(arrow), Write(label))
            self.wait(1)

            # Remove arrow and text
            self.play(FadeOut(arrow), FadeOut(glow_arrow), FadeOut(label), FadeOut(glow_label))

        # Step 1: Customer enters information in UX
        sequence_step(ux, domain_api, "Customer enters payment info", BLUE)

        # Step 2: UX sends request to Domain API Layer for validation
        sequence_step(domain_api, microvalidator, "Domain API validates payment info", GREEN)

        # Step 3: Domain API sends request to MicroValidator for validation
        sequence_step(microvalidator, domain_api, "MicroValidator validates Debtor & Creditor info", YELLOW)

        # Step 4: MicroValidator calls internal services
        services = [
            "DebtorAccEnrich", "AccessTypeLookup", "CreditorAccEnrich",
            "IbanLookup", "ValidateBBAN", "TransactionIdentificationControl",
            "CutoffBD", "TransactionExecutionService"
        ]
        for service in services:
            service_text = Text(f"Call {service}", font_size=14, color=ORANGE).move_to(ORIGIN)
            glow_service_text = service_text.copy().set_opacity(0.3).set_color(WHITE)
            self.play(FadeIn(glow_service_text), FadeIn(service_text))
            self.wait(0.5)
            self.play(FadeOut(glow_service_text), FadeOut(service_text))

        # Step 5: MicroValidator responds with ACCP
        sequence_step(microvalidator, domain_api, "Response: ACCP", YELLOW)

        # Step 6: Domain API sends data to UX and creates pain.001
        sequence_step(domain_api, ux, "Send data to UX", GREEN)
        sequence_step(domain_api, ftm, "Create and send pain.001", RED)

        # Step 7: FTM processes pain.001 and maps it
        subtask1 = Text("Map pain.001", font_size=16, color=RED).move_to(ORIGIN)
        glow_subtask1 = subtask1.copy().set_opacity(0.3).set_color(WHITE)
        self.play(FadeIn(glow_subtask1), FadeIn(subtask1))
        self.wait(1)
        self.play(FadeOut(glow_subtask1), FadeOut(subtask1))

        # Step 8: FTM validates using MicroValidator's lookup service
        subtask2 = Text("Validation via lookup service", font_size=16, color=YELLOW).move_to(ORIGIN)
        glow_subtask2 = subtask2.copy().set_opacity(0.3).set_color(WHITE)
        self.play(FadeIn(glow_subtask2), FadeIn(subtask2))
        self.wait(1)
        self.play(FadeOut(glow_subtask2), FadeOut(subtask2))

        # Step 9: FTM waits for customer approval
        approval_text = Text("Waiting for customer approval", font_size=20, color=RED).move_to(ORIGIN)
        glow_approval_text = approval_text.copy().set_opacity(0.3).set_color(WHITE)
        self.play(FadeIn(glow_approval_text), FadeIn(approval_text))
        self.wait(2)
        self.play(FadeOut(glow_approval_text), FadeOut(approval_text))

        # Hold the final frame
        self.wait(2)
