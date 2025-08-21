아래의 체육관 사이트들에서
내가 설계할 파이썬 프로그램은 다음과 같다.
아이디/비번을 입력하면 자동으로 로그인하고
미리 예약시작시간, 예약날짜, 시작시간, 연락처, 소속, 학번, 사용기간 (1시간, 2시간 중에서), 이용자수(숫자만), 이용자 명단(27자 이상), 행사계획(15자 이상)을 입력한다.
이후 예약시간에 예약 날짜로 URL로 바로 접근한 다음(25년 8월 28일 예약 URL은 날짜부분만 바뀌어서, https://sports.knu.ac.kr/doc/class_info6_time.php?&tDATE=2025-08-28&fc_grno=1&fc_sqno=1#this 이다.), 시작시간을 자동 선택해 다음 페이지로 간다.
그 페이지에서 연락처, 소속, 학번, 사용기간, 이용자수, 이용자 명단, 행사계획을 자동 입력하고 다음단계로 넘어간다.
다음단계로 넘어가면 성공메세지를 출력하고 프로그램은 초기화된다.
프로그램 코드를 작성하여라.
작업 시, "Patch Notes.md"도 읽어 작업지시사항이 이전의 문제점과 충돌할 경우 작업방향을 수정, 보완하도록 한다.
작업 후, 지시사항, 작업방향 수정내용(수정 했을 경우)과 작업내용을 "Patch Notes.md"의 기존양식에 맞춰, 기존내용 아래에 추가 업데이트하도록 한다. 


체육관사이트의 로직은 다음과 같다.
https://sports.knu.ac.kr/pages/member/login.php에서 
아이디/비밀번호를 
<tr>
								 <td class="txtid">아이디</td>
								 <td><input class="input230" maxlength="20" size="20" name="id" itemname="아이디" minlength="2" tabindex="1"></td>
								 <td rowspan="2"><p class="submitRow"><input type="submit" src="" value="로그인" class="login" onclick="CheckLogin();" tabindex="3"></p></td>
							   </tr>

<tr>
								 <td class="txtid">비밀번호</td>
								 <td><input class="input230" type="password" maxlength="20" size="20" name="password" itemname="패스워드" tabindex="2"></td>
							   </tr>
으로 입력한다.

이후 https://sports.knu.ac.kr/doc/class_info6.php?fc_grno=1에서
<li class=""><a href="#tab4">예약하기</a></li>를 누른다.

캘린더 박스는 다음과 같다. 여기서 해당하는 월로 캘린더를 이동후 해당하는 날짜 (예약가능)를 선택하면 

<div id="cal_box">
					   
					   <p class="txt_m">
					   <span><a href="#this" onclick="changeCalendar('PREV')">&lt;</a>&nbsp;&nbsp;</span>
					   <span id="CURDATE">2025-08</span>
					   <span>&nbsp;&nbsp;<a href="#this" onclick="changeCalendar('NEXT')">&gt;</a></span></p>

						<div id="LOADING" style="background-color:#f7f7f7;width:750px;height:200px;position:absolute;top:100;left:350;display:none;z-index:1000">
						<table width="100%">
							<tbody><tr>
								<td align="center" height="200"><img src="../pages/board/images/ajax_loding.gif" alt="로딩중입니다"><br>달력을 갱신중입니다.. 잠시만 기다려 주세요!</td>
							</tr>
						</tbody></table>
						</div>
						<table class="calendar" id="CALENDAR">
						  <colgroup>
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                        <col style="width:14.2%">
                    </colgroup>
                      <tbody><tr>
                          <th class="sun">일</th>
                          <th>월</th>
                          <th>화</th>
                          <th>수</th>
                          <th>목</th>
                          <th>금</th>
                          <th class="sat">토</th>
                      </tr><tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><p>1</p><p class="mtion sun">예약불가</p></td>
<td class="sat"><p>2</p><p class="mtion sun">예약불가</p></td>
</tr>
<tr>
<td class="sun"><p>3</p><p class="mtion sun">예약불가</p></td>
<td><p>4</p><p class="mtion sun">예약불가</p></td>
<td><p>5</p><p class="mtion sun">예약불가</p></td>
<td><p>6</p><p class="mtion sun">예약불가</p></td>
<td><p>7</p><p class="mtion sun">예약불가</p></td>
<td><p>8</p><p class="mtion sun">예약불가</p></td>
<td class="sat"><p>9</p><p class="mtion sun">예약불가</p></td>
</tr>
<tr>
<td class="sun"><p>10</p><p class="mtion sun">예약불가</p></td>
<td><p>11</p><p class="mtion sun">예약불가</p></td>
<td><p>12</p><p class="mtion sun">예약불가</p></td>
<td><p>13</p><p class="mtion sun">예약불가</p></td>
<td><p>14</p><p class="mtion sun">예약불가</p></td>
<td><p>15</p><p class="mtion sun">예약불가</p></td>
<td class="sat"><p>16</p><p class="mtion sun">예약불가</p></td>
</tr>
<tr>
<td class="sun"><p>17</p><p class="mtion sun">예약불가</p></td>
<td><p>18</p><p class="mtion sun">예약불가</p></td>
<td><p>19</p><p class="mtion sun">예약불가</p></td>
<td style="background-color:#e8e8e8"><p>20</p><p class="mtion sun">예약불가</p></td>
<td><p>21</p><p class="mtion sun">예약불가</p></td>
<td><p>22</p><p class="mtion sun">예약불가</p></td>
<td class="sat"><p>23</p><p class="mtion sun">예약불가</p></td>
</tr>
<tr>
<td class="sun"><p>24</p><p class="mtion sun">예약불가</p></td>
<td><p>25</p><p class="mtion sun">예약불가</p></td>
<td><p>26</p><p class="mtion sun">예약불가</p></td>
<td><p>27</p><p class="mtion"><a href="class_info6_time.php?&amp;tDATE=2025-08-27&amp;fc_grno=1&amp;fc_sqno=1">예약가능</a></p></td>
<td><p>28</p><p class="mtion"><a href="class_info6_time.php?&amp;tDATE=2025-08-28&amp;fc_grno=1&amp;fc_sqno=1">예약가능</a></p></td>
<td><p>29</p><p class="mtion"><a href="class_info6_time.php?&amp;tDATE=2025-08-29&amp;fc_grno=1&amp;fc_sqno=1">예약가능</a></p></td>
<td class="sat"><p>30</p><p class="mtion"><a href="class_info6_time.php?&amp;tDATE=2025-08-30&amp;fc_grno=1&amp;fc_sqno=1">예약가능</a></p></td>
</tr>
<tr>
<td class="sun"><p>31</p><p class="mtion"><a href="class_info6_time.php?&amp;tDATE=2025-08-31&amp;fc_grno=1&amp;fc_sqno=1">예약가능</a></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
					   </tbody></table>
				  </div>


다음과 같이 동의 버튼을 누르고,
<input type="checkbox" style="margin-left:298px;?&gt;" class="radio" name="agree" value="Y" id="agree">
시작시간버튼으로 선택할 수 있다
<li>
							<span class="timebox_on"><a href="#this" onclick="reserveFacility('7')">7시</a></span><span class="timebox_on"><a href="#this" onclick="reserveFacility('8')">8시</a></span><span class="timebox_on"><a href="#this" onclick="reserveFacility('9')">9시</a></span><span class="timebox_off">10시</span><span class="timebox_off">11시</span><span class="timebox_off">12시</span><span class="timebox_off">13시</span><span class="timebox_off">14시</span><span class="timebox_off">15시</span><span class="timebox_off">16시</span><span class="timebox_off">17시</span><span class="timebox_off">18시</span><span class="timebox_off">19시</span><span class="timebox_off">20시</span><span class="timebox_off">21시</span>					     
						  </li>

시작시간을 선택해 클릭하면 다음 칸에 정보를 채워 넣어야 한다.
				  <th>연락처</th>
				  <td><input type="text"  class="input200" name="HP_NO" value="" maxlength="20" autocomplete='off' />
<a href="#none">&nbsp;</a>				  
				  </td>
			  </tr>
			  <tr>
				  <th>소속</th>
				  <td><input type="text"  class="input200" name="BLNG_NM" value="" maxlength="20" autocomplete='off' />
<a href="#none">&nbsp;</a>					  
				  </td>
			  </tr>
			  <tr>
				  <th>학번</th>
				  <td><input type="text"  class="input200" name="EMNO" value=""  maxlength="20" autocomplete='off' /></td>
			  </tr>
			  <tr>
				  <th>사용기간 </th>
				  <td> <span class="fc_06 bold">2025년08월29일</span> 8시 부터 
				  <select name="use_time"  class="select80 ml5" onchange="calcAMT(this)">
					<option value="">-선택-</option>
                                                                              <option value="1">1시간</option>
                                                        <option value="2">2시간</option>
                                                
				  </select>
				  <!-- <span class="fc_01">- 이용금액 : <span id="USE_AMT">0원</span></span> -->

                            <ul class="note_per">
                                                                                                <li>한 팀당 주 1회, 최대 2시간 신청가능</li>
                                
						   <li>학과 및 단과대학 규모 이상의 행사는 사전 협의 후 신청 가능</li>
						</ul>
				  </td>
			  </tr>
			  <tr>
				  <th>이용자수</th>
				  <td><input type="text"  class="input50" name="USER_QTY" value="" maxlength="3" onkeyup="CheckNumber(this)" autocomplete='off' /> 명</td>
			  </tr>
			  <tr>
				  <th>이용자 명단</th>
				  <td><textarea  class="textarea95" name="USER_LIST" autocomplete='off'></textarea>
				   <p class="fc_05 note_style1" >
				   대표자 포함하여 이용자의 소속, 성명, 인원수 입력(대운동장의 경우 최소10명)
<!-- 대운동장은 해당팀의 성명, 학번, 연락처(최소 10명)의 상대팀의 소속, 성명을 입력<br>(기타 시설은 대표자외 동반하여 운동하는 인원의 소속, 인원을 입력)  --></p>
				  </td>
			  </tr>
			  <tr>
				  <th>행사계획</th>
				  <td><textarea  class="textarea95" name="EVNT_PLAN" autocomplete='off'></textarea>
				   <p class="fc_05 note_style1" >시간별  행사계획, 이용 후 청소계획, 이용인원 통제(주차포함) 계획을 입력</p></td>
			  </tr>
			</table>
			<p class="submitRow mt30"><input type="button" value="다음단계" class="input1 mr8" onclick="checkFacility()" /><input type="submit" value="뒤로가기" class="cancel" /></p>
				<!-- //예약정보 입력하기  -->
</form>
				</div>				

				</div>
		  </div><!--//tab_container1-->
	  
	  </div><!--//tab_container-->
	  <!--  이용안내 End  -->

이후 <input type="button" value="다음단계" class="input1 mr8" onclick="checkFacility()">와 같은 다음단계를 클릭하면  일단 완성이다.
