# THIRD SCHEDULE

Sections 20 and 21, paragraph 1 of the Second Schedule and paragraph 1 of the Fourth Schedule

DIGITAL SIGNATURES

PART I

GENERAL

Interpretation

1.—(1) In this Schedule, unless the context otherwise requires —

“accredited certification authority” means a certification authority accredited by the Controller pursuant to any regulations made under section 22;

“asymmetric cryptosystem” means a system capable of generating a secure key pair, consisting of a private key for creating a digital signature, and a public key to verify the digital signature;

“certificate” means a record issued for the purpose of supporting digital signatures which purports to confirm the identity or other significant characteristics of the person who holds a particular key pair;

“certification authority” means a person who issues a certificate;

“certification practice statement” means a statement issued by a certification authority to specify the practices that the certification authority employs in issuing certificates;

“correspond”, in relation to a private key or public key, means to belong to the same key pair;

THIRD SCHEDULE — continued

“digital signature” means an electronic signature consisting of a transformation of an electronic record using an asymmetric cryptosystem and a hash function such that a person having the initial untransformed electronic record and the signer’s public key can accurately determine —

(a) whether the transformation was created using the private key that corresponds to the signer’s public key; and

(b) whether the initial electronic record has been altered since the transformation was made;

“hash function” means an algorithm mapping or translating one sequence of bits into another, generally smaller, set (the hash result) such that —

(a) a record yields the same hash result every time the algorithm is executed using the same record as input;

(b) it is computationally infeasible that a record can be derived or reconstituted from the hash result produced by the algorithm; and

(c) it is computationally infeasible that 2 records can be found that produce the same hash result using the algorithm;

“key pair”, in an asymmetric cryptosystem, means a private key and its mathematically related public key, having the property that the public key can verify a digital signature that the private key creates;

“operational period”, in relation to a certificate, means a period beginning on the date and time the certificate is issued by a certification authority (or on a later date and time if stated in the certificate), and ending on the date and time the certificate expires (as stated in the certificate) or is earlier revoked or suspended;

“private key” means the key of a key pair used to create a digital signature;

“public key” means the key of a key pair used to verify a digital signature;

“recognised certificate” means a certificate recognised pursuant to regulations made under section 22(3);

“recognised certification authority” means a certification authority recognised pursuant to regulations made under section 22(3);

“repository” means a system for storing and retrieving certificates or other information relevant to certificates;

“revoke”, in relation to a certificate, means to permanently end the operational period of the certificate from a specified time;

THIRD SCHEDULE — continued

“subscriber” means a person who is the subject named or identified in a certificate issued to him and who holds a private key that corresponds to a public key listed in that certificate;

“suspend”, in relation to a certificate, means to temporarily suspend the operational period of the certificate from a specified time;

“trustworthy system” means computer hardware, software and procedures that —

(a) are reasonably secure from intrusion and misuse;

(b) provide a reasonable level of availability, reliability and correct operation;

(c) are reasonably suited to performing their intended functions; and

(d) adhere to generally accepted security procedures;

“valid certificate” means a certificate that a certification authority has issued and which the subscriber listed in it has accepted;

“verify a digital signature”, in relation to a given digital signature, record and public key, means to determine accurately that —

(a) the digital signature was created using the private key corresponding to the public key listed in the certificate; and

(b) the record has not been altered since its digital signature was created.

(2) In the application of this Act to certificates issued by the Controller and digital signatures verified by reference to those certificates, the Controller shall be deemed to be an accredited certification authority.

Secure electronic record with digital signature

2. The portion of an electronic record that is signed with a digital signature shall be treated as a secure electronic record if the digital signature is a secure electronic signature by virtue of paragraph 3.

Digital signature treated as secure electronic signature

3. When any portion of an electronic record is signed with a digital signature, the digital signature shall be treated as a secure electronic signature with respect to such portion of the record, if —

(a) the digital signature was created during the operational period of a valid certificate and is verified by reference to the public key listed in such certificate; and

THIRD SCHEDULE — continued

(b) the certificate is considered trustworthy, in that it is an accurate binding of a public key to a person’s identity because —

(i) the certificate was issued by an accredited certification authority operating in compliance with the regulations made under section 22;

(ii) the certificate was issued by a recognised certification authority;

(iii) the certificate was issued by a public agency approved by the Minister to act as a certification authority on such conditions as he may by regulations impose or specify; or

(iv) the parties have expressly agreed between themselves (sender and recipient) to use digital signatures as a security procedure, and the digital signature was properly verified by reference to the sender’s public key.

Presumptions regarding certificates

4. It shall be presumed, unless evidence to the contrary is adduced, that the information (except for information identified as subscriber information which has not been verified) listed in a certificate issued by an accredited certification authority or a recognised certification authority, or in a recognised certificate, is correct if the certificate was accepted by the subscriber.

Unreliable digital signatures

5. Unless otherwise provided by law or contract, a person relying on a digitally signed electronic record assumes the risk that the digital signature is invalid as a signature or an authentication of the signed electronic record, if reliance on the digital signature is not reasonable under the circumstances having regard to the following factors:

(a) facts which the person relying on the digitally signed electronic record knows or has notice of, including all facts listed in the certificate or incorporated in it by reference;

(b) the value or importance of the digitally signed electronic record, if known;

(c) the course of dealing between the person relying on the digitally signed electronic record and the subscriber and any available indicia of reliability or unreliability apart from the digital signature; and

(d) any usage of trade, particularly trade conducted by trustworthy systems or other electronic means.

THIRD SCHEDULE — continued

Reliance on certificates foreseeable

6. It is foreseeable that persons relying on a digital signature will also rely on a valid certificate containing the public key by which the digital signature can be verified.

Prerequisites to publication of certificate

7. No person may publish a certificate or otherwise make it available to a person known by that person to be in a position to rely on the certificate or on a digital signature that is verifiable with reference to a public key listed in the certificate, if that person knows that —

(a) the certification authority listed in the certificate has not issued it;

(b) the subscriber listed in the certificate has not accepted it; or

(c) the certificate has been suspended or revoked, unless such publication is for the purpose of verifying a digital signature created prior to such suspension or revocation.

Publication for fraudulent or unlawful purpose

8. Any person who knowingly creates, publishes or otherwise makes available a certificate for any fraudulent or unlawful purpose shall be guilty of an offence and shall be liable on conviction to a fine not exceeding $20,000 or to imprisonment for a term not exceeding 2 years or to both.

False or unauthorised request

9. Any person who knowingly misrepresents to a certification authority his identity or authorisation for the purpose of requesting for a certificate or for suspension or revocation of a certificate shall be guilty of an offence and shall be liable on conviction to a fine not exceeding $10,000 or to imprisonment for a term not exceeding 6 months or to both.

Recommended reliance limit

10.—(1) An accredited certification authority or a recognised certification authority shall, in issuing a certificate to a subscriber, specify a recommended reliance limit in the certificate.

(2) The accredited certification authority or recognised certification authority may specify different reliance limits in different certificates as it considers fit.

THIRD SCHEDULE — continued

Liability limits for accredited certification authorities

11. Unless an accredited certification authority or a recognised certification authority waives the application of this paragraph, an accredited certification authority or a recognised certification authority shall not be liable —

(a) for any loss caused by reliance on a false or forged digital signature of a subscriber, if, with respect to the false or forged digital signature, the accredited certification authority or recognised certification authority complied with the requirements of this Act; or

(b) in excess of the amount specified in the certificate as its recommended reliance limit for either —

(i) a loss caused by reliance on a misrepresentation in the certificate of any fact that the accredited certification authority or recognised certification authority is required to confirm; or

(ii) failure to comply with paragraphs 14 and 15 in issuing the certificate.

PART II

DUTIES OF CERTIFICATION AUTHORITY

Trustworthy system

12. A certification authority must utilise trustworthy systems in performing its services.

Disclosure

13.—(1) A certification authority shall disclose —

(a) its certificate that contains the public key corresponding to the private key used by that certification authority to digitally sign another certificate (referred to in this paragraph as a certification authority certificate);

(b) any relevant certification practice statement;

(c) notice of the suspension or revocation of its certification authority certificate; and

(d) any other fact that materially and adversely affects either the reliability of a certificate that the authority has issued or the authority’s ability to perform its services.

THIRD SCHEDULE — continued

(2) In the event of an occurrence that materially and adversely affects a certification authority’s trustworthy system or its certification authority certificate, the certification authority shall —

(a) use reasonable efforts to notify any person who is known to be or foreseeably will be affected by that occurrence; or

(b) act in accordance with procedures governing such an occurrence specified in its certification practice statement.

Issuance of certificate

14.—(1) A certification authority may issue a certificate to a prospective subscriber only after the certification authority —

(a) has received a request for issuance from the prospective subscriber; and

(b) has —

(i) if it has a certification practice statement, complied with all of the practices and procedures set forth in such certification practice statement including procedures regarding identification of the prospective subscriber; or

(ii) in the absence of a certification practice statement, complied with the conditions in sub‑paragraph (2).

(2) In the absence of a certification practice statement, the certification authority shall confirm by itself or through its authorised agent that —

(a) the prospective subscriber is the person to be listed in the certificate to be issued;

(b) if the prospective subscriber is acting through one or more agents, the subscriber authorised the agent to have custody of the subscriber’s private key and to request issuance of a certificate listing the corresponding public key;

(c) the information in the certificate to be issued is accurate;

(d) the prospective subscriber rightfully holds the private key corresponding to the public key to be listed in the certificate;

(e) the prospective subscriber holds a private key capable of creating a digital signature; and

(f) the public key to be listed in the certificate can be used to verify a digital signature affixed by the private key held by the prospective subscriber.

THIRD SCHEDULE — continued

Representations upon issuance of certificate

15.—(1) By issuing a certificate, a certification authority represents to any person who reasonably relies on the certificate or a digital signature verifiable by the public key listed in the certificate that the certification authority has issued the certificate in accordance with any applicable certification practice statement incorporated by reference in the certificate, or of which the relying person has notice.

(2) In the absence of such certification practice statement, the certification authority represents that it has confirmed that —

(a) the certification authority has complied with all applicable requirements of this Act in issuing the certificate, and if the certification authority has published the certificate or otherwise made it available to such relying person, that the subscriber listed in the certificate has accepted it;

(b) the subscriber identified in the certificate holds the private key corresponding to the public key listed in the certificate;

(c) the subscriber’s public key and private key constitute a functioning key pair;

(d) all information in the certificate is accurate, unless the certification authority has stated in the certificate or incorporated by reference in the certificate a statement that the accuracy of specified information is not confirmed; and

(e) the certification authority has no knowledge of any material fact which if it had been included in the certificate would adversely affect the reliability of the representations in sub‑paragraphs (a) to (d).

(3) Where there is an applicable certification practice statement which has been incorporated by reference in the certificate, or of which the relying person has notice, sub‑paragraph (2) shall apply to the extent that the representations are not inconsistent with the certification practice statement.

Suspension of certificate

16. Unless the certification authority and the subscriber agree otherwise, the certification authority that issued a certificate shall suspend the certificate as soon as possible after receiving a request by a person whom the certification authority reasonably believes to be —

(a) the subscriber listed in the certificate;

(b) a person duly authorised to act for that subscriber; or

(c) a person acting on behalf of that subscriber, who is unavailable.

THIRD SCHEDULE — continued

Revocation of certificate

17. A certification authority shall revoke a certificate that it issued —

(a) after receiving a request for revocation by the subscriber listed in the certificate; and confirming that the person requesting the revocation is the subscriber, or is an agent of the subscriber with authority to request the revocation;

(b) after receiving a certified copy of the subscriber’s death certificate, or upon confirming by other evidence that the subscriber is dead; or

(c) upon presentation of documents effecting a dissolution of the subscriber, or upon confirming by other evidence that the subscriber has been dissolved or has ceased to exist.

Revocation without subscriber’s consent

18.—(1) A certification authority shall revoke a certificate, regardless of whether the subscriber listed in the certificate consents, if the certification authority confirms that —

(a) a material fact represented in the certificate is false;

(b) a requirement for issuance of the certificate was not satisfied;

(c) the certification authority’s private key or trustworthy system was compromised in a manner materially affecting the certificate’s reliability;

(d) an individual subscriber is dead; or

(e) a subscriber has been dissolved, wound up or otherwise ceased to exist.

(2) Upon effecting such a revocation, other than under sub‑paragraph (1)(d) or (e), the certification authority shall immediately notify the subscriber listed in the revoked certificate.

Notice of suspension

19.—(1) Immediately upon suspension of a certificate by a certification authority, the certification authority shall publish a signed notice of the suspension in the repository specified in the certificate for publication of notice of suspension.

(2) Where one or more repositories are specified, the certification authority shall publish signed notices of the suspension in all such repositories.

THIRD SCHEDULE — continued

Notice of revocation

20.—(1) Immediately upon revocation of a certificate by a certification authority, the certification authority shall publish a signed notice of the revocation in the repository specified in the certificate for publication of notice of revocation.

(2) Where one or more repositories are specified, the certification authority shall publish signed notices of the revocation in all such repositories.

PART III

DUTIES OF SUBSCRIBERS

Generating key pair

21.—(1) If the subscriber generates the key pair whose public key is to be listed in a certificate issued by a certification authority and accepted by the subscriber, the subscriber shall generate that key pair using a trustworthy system.

(2) This paragraph shall not apply to a subscriber who generates the key pair using a system approved by the certification authority.

Obtaining certificate

22. All material representations made by the subscriber to a certification authority for purposes of obtaining a certificate, including all information known to the subscriber and represented in the certificate, shall be accurate and complete to the best of the subscriber’s knowledge and belief, regardless of whether such representations are confirmed by the certification authority.

Acceptance of certificate

23.—(1) A subscriber shall be deemed to have accepted a certificate if he —

(a) publishes or authorises the publication of the certificate —

(i) to one or more persons; or

(ii) in a repository; or

(b) otherwise demonstrates approval of the certificate while knowing or having notice of its contents.

(2) By accepting a certificate issued by himself or a certification authority, the subscriber listed in the certificate certifies to all who reasonably rely on the information contained in the certificate that —

(a) the subscriber rightfully holds the private key corresponding to the public key listed in the certificate;

THIRD SCHEDULE — continued

(b) all representations made by the subscriber to the certification authority and material to the information listed in the certificate are true; and

(c) all information in the certificate that is within the knowledge of the subscriber is true.

Control of private key

24.—(1) By accepting a certificate issued by a certification authority, the subscriber identified in the certificate assumes a duty to exercise reasonable care to retain control of the private key corresponding to the public key listed in such certificate and prevent its disclosure to a person not authorised to create the subscriber’s digital signature.

(2) Such duty shall continue during the operational period of the certificate and during any period of suspension of the certificate.

Initiating suspension or revocation of certificate

25. A subscriber who has accepted a certificate shall as soon as possible request the issuing certification authority to suspend or revoke the certificate if the private key corresponding to the public key listed in the certificate has been compromised.

[ETA, ss. 2, 19 to 40, 41(5), 44 and 45]
