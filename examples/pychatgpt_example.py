from pyChatGPT import ChatGPT

# `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..u5OgiMUov_JxkzSl.84yBsbn7aMZ9iw_s3VGGM7cBtwJspr38z-g5bK0fDILGUiBEY4TDCBomEyhul1SP_KB4kOsl_gllXknJoxHswvVRKer6RjKeOUsdXQVP3KbdpnB4NrAA9qBjIr3CY6_1WSTb7p7mOMhLQeaSOVgdw_t5rWfZyPiwnm7qJIO1ItNCZzNIT2MMWvad2LZztwk9-erAo70wsGnDJFXm1iF3kqTx9XEOyo9e5mXe_dIPYPMzHS_O83eyIE3ntxlPIQpL9QJIotW79ajIcW0EhQ4pSxdReprnQs59_9_7Fv5bg5FMGuv1QJRzef2jXVi5MXIN8-SR5m4bo0WAV-X_fCPEndu5p1_LWv2_PI0_WDgM6h6iTrnxbUSR6_Ih3ZmdiCbTG8oLbX49JPwogTPuRAJrdgLvNi0fe3YKZ5XbybwaKLgupiRWXC3MWwBr7satX5gcMnPYEg8oc-otQHKKPMHB9kMt2qvjG3Kv2vFGLgtbSmhMcBnprA01l1esxBCjXQU7_H1n5LDI5JciFNIC-AonK_7k8EQCdHz9EmZHG1Z042CyvGIkuM2p81wb7EezeWisHVcdaG1t8BdM7U1IrObG6E0WSi8zgvwZVgXIv0jcx93756XaOr2Mxw82iyKWXTBOYqQhjOeXGk8IqcWr-FrPGkEa2ZuiwZcJ7ze55JDEDh95uzo5fz08Ij05hJyfzhfzT6r3XLaMfQ6yCamabW4NQ0AJHF6W_lpmCfmCAjNj3MMD3Ww-CcCYLDPJGo0L512xl_yYxxpQROqxQMFdfe8EHTT8dK5rqStjVXzDRMPWuPUSnEtlKvoqBEqNRo9q6rfwgFdMB6LY8YW2BI2jypnCS7NvzvDAmXH-QDga-6UpcXL6NwhAd2Pq8Y8S45Trhy5Y3-Vpcn-RvDvEYFvLXBkqcAq43S326YwRdpd3tspOqM-qYvXSLSqLwOQ2IYpntXY58Pl3_9NrVEE_qnfjGh59poLfEq5qs4g0pEU2IprEzBlwco_Bualz6Uu7zqveW331JiX5EeX5uOjqmSSAGhHkZBGmorzFn94-Gbe-q4mL-Vw_jvrvwKNi_5qQaVhAT8OEmlY5Wn8uo3b0r0Lj1pyC8tjsxp2neJnhbBB0nA-jMYTjkakXqA0ysQUnKcYlZgtfusNDc6-UOXIikunyKyGauufmDR7XFtU7UFBhTTiyTi0aO7g2kFvlxhaYG5TnPFBWyq0ff8uYsIzhs4X3PE6y4edlVjraBdpteKWIphS4Px6-K-3QW6tCgqOA0Rt86EPRHyieJxScFch5eBAfacf6MPoMTaCI-NAp1WmhmEAb50OhsTKN63fpm2RhC6cJHKDh78Zwqtl5tsgUWfF9ie8b9yXghy6O6dKzonmtsyEDd4nxve-DUlCJJhaCWgKkHa9VBFb6rLuAKh4-Hng7OR_NBOhxBeS8CIplrPI6a8zTTk1BI-tUlOA8__ADx5evbfezZIuqQFd8HHcfHqj4-5SRRgmPAkBrV8_zN6vYY6jaUVKTes1sEkG-Pv3yPwHM6r_K7oZSMbRbGNn3DATe44p781mMwuGXDlNFw5wbWaELCiUYks2HHIXLkSAMI27bcebHjz2KW5WI91mfz8JsRpfISo8RUoRcsoUkWXjANAL4YWL0CeVao-12cry-VBabL0nyMm7A7qFhu85S_9texXq9lzpCxfe-uu0U213_Lsgfh34qSQRSSNpLjY-8ZlYws75V1YCeGI3LvhjGeZNq3OBj4DbjhV9hekJ8gmlTQw_W_y88QSpLVPvI0v7SLXHdnDgxFirz27TUP0OPvi6N0wIewfBuzIZyqZMAnXK3ymi0Ve8acCdTCLQ3r6IUZVbKT0YP3jT8gko_02nV2khKJlQHhISFOd-imipuBrZTAwMoXljceg0Xp3oHBpjq3rLK_Vol4Z2MeImlF8tGOugaBR9qL2tmTjPhsaATHJ6Ts5mEOPNsP4rDRi5f77k7nN86A5DYEUKNl5mLKEqKs3QtUaobRtXZM10fosXfXNzBASgmH6hyPOMzmkS86F_Nge9-EX1cGG_ElXULPfyqO7H_zfkaLFI_YSLMwmVH2ztV-YEYH8o7vJl-XhHebDtKGPD4r63_QazSEI0cJKelBEQkLu3U8ATDJQ9R04qhsYQ3vEFs7vjMJMQOb9iHHsoUp0LPx2oui_mkP60zWNNgjY6r_chGvsbv4INPDrLF1pwYJ5WsQxXfG9uhKewcpkFiTkQZNeYAXRM2JGNRC5cWDi92WxekmNO5i-hxDR_4pu-ko90LMPThzcls9PHurkTjoajpWyMg33guNitPW6lb58DhKyvaYMZ8xBveDkhKTjmjdj8ELfMBXj06wbXIe7JesudVziahJw6RiLVJfl5732kpNkoolqVfagnQzFkef1gx4Q9j6NAAMGKJ_pkx7tjfwtyzzdiajdojd3Jg_jBGbVfozVTb0_r2zHGWISRfijN40zWoLQxpXWZx2najKH8v7nNj0mJxQ6ssCNk65Ntd45Ouixj3-p_hMJ2oBD3njxKQQW0umSuWI_Y7-xximlsGGKhZHme5KfFDfmUgyi874wGO9kQSGoF8Bk7kvXgU_38YE_ZzBR7vk_zUdvQL3T6T9vJGMmi8o6bRb79clK8edVE9YivuUg.yfVAWCb3_tV2T72Ex3z9Hw'
# api = ChatGPT(session_token)  # auth with session token
# api = ChatGPT(session_token, conversation_id='some-random-uuid')  # specify conversation id
# api = ChatGPT(session_token, proxy='https://proxy.example.com:8080')  # specify proxy
# api = ChatGPT(session_token, chrome_args=['--window-size=1920,768'])  # specify chrome args
api = ChatGPT(session_token, moderation=False)  # disable moderation
# api = ChatGPT(session_token, verbose=True)  # verbose mode (print debug messages)

# auth with google login
api = ChatGPT(auth_type='google', email='example@gmail.com', password='password')
# auth with microsoft login
api = ChatGPT(auth_type='microsoft', email='example@gmail.com', password='password')
# auth with openai login (captcha solving using speech-to-text engine)
api = ChatGPT(auth_type='openai', email='example@gmail.com', password='password')
# auth with openai login (manual captcha solving)
api = ChatGPT(
    auth_type='openai', captcha_solver=None, # type: ignore
    email='example@gmail.com', password='password'
)
# auth with openai login (2captcha for captcha solving)
api = ChatGPT(
    auth_type='openai', captcha_solver='2captcha', solver_apikey='abc',
    email='example@gmail.com', password='password'
)
# reuse cookies generated by successful login before login,
# if `login_cookies_path` does not exist, it will process logining  with `auth_type`, and save cookies to `login_cookies_path`
# only works when `auth_type` is `openai` or `google`
api = ChatGPT(auth_type='openai', email='example@xxx.com', password='password',
    login_cookies_path='your_cookies_path',
)

resp = api.send_message('Hello, world!')
print(resp['message'])

api.reset_conversation()  # reset the conversation
api.clear_conversations()  # clear all conversations
api.refresh_chat_page()  # refresh the chat page